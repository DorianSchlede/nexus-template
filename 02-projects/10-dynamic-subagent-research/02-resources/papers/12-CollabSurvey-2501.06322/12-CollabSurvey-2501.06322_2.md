<!-- Source: 12-CollabSurvey-2501.06322.pdf | Chunk 2/7 -->

**3** **Multi-Agent Collaboration Concept**

We introduce the main concepts of LLM-based multi-agent collaborative systems, defining key
components of agents, systems, and collaboration mechanisms based on insights from recent
research in this emerging area.


**3.1** **Agent and Collaborative System Definition**


An agent can be mathematically represented by _𝑎_ = { _𝑚,𝑜,𝑒,𝑥,𝑦_ } as follows:


  - Model _𝑚_ = {arch _,_ mem _,_ adp}: the AI model, consisting of its architecture (arch), agent’s
specific memory (mem), and optional adapters (adp). Adapters are adaptive intelligent
modules that allow the agent to incorporate additional knowledge from others through
mechanisms such as speculative decoding and parameter-efficient adapter, which can
further enrich the model’s response capabilities [40, 72, 98]. In the case of LLM agents, the
architecture arch is a language model, and the agent’s specific memory mem is typically
the system prompt _𝑟_ .

   - Objective _𝑜_ : the objective or goal of the agent, guiding its actions within the system. For example, in question-answering tasks, the objective is to minimize the cross-entropy between
the generated answer and the ground truth.


8 Tran et al.


  - Environment _𝑒_ : the environment or context encompassing the state or conditions in which
the agent operates. In LLM, usually the context window is constrained by the number of
tokens.

  - Input _𝑥_ : input perception, such as text or sensor data. In LLM, _𝑥_ is encoded as a sequence of
tokens.

  - Output _𝑦_ : the corresponding action or output, defined by the function _𝑦_ = _𝑚_ ( _𝑜,𝑒,𝑥_ ), where
the agent uses its model, context, and objective to act on the input _𝑥_ .


LLM-based agents are typically pre-trained on diverse datasets to provide a strong foundational
knowledge base. This pre-training process equips an individual agent with essential skills and
understanding, ensuring they can meaningfully contribute to the collaborative environment. Moreover, each agent can also be equipped with external tools unique to their own, such as Calculator
and Python interpreter.
When generalized to a multi-agent collaborative system _𝑆_, it includes the following:


  - A = { _𝑎𝑖_ } _[𝑛]_ _𝑖_ =1 [: LLM-based agents, where] _[ 𝑛]_ [is the number of agents, which is pre-defined or]
adjusted dynamically depending on the current requirements of the system.

  - O _𝑐𝑜𝑙𝑙𝑎𝑏_ : a collective set of goals that may be partitioned into unique objectives for each
agent, ensuring alignment with the overall system goal.

   - E: a shared environment from which agents receive contextual data. In our case of an
LLM-based MAS, the environment may take various forms, such as vector-based databases
or common messaging interfaces.

  - C = { _𝑐_ _𝑗_ }: a set of collaboration channels that facilitate interactions among agents, enabling
the exchange of information based on given objectives, environment, and inputs: _𝑦_ _𝑗_ =
_𝑐_ _𝑗_ ({ _𝑎𝑖_ ( _𝑜𝑖,_ E _,𝑥𝑖_ )| _𝑎𝑖,𝑜𝑖,𝑥𝑖_ ∈ _𝑐_ _𝑗_ }). Channels are distinguished by their mechanisms, including
actors (agents), types, structures, and strategies. If two channels differ in these aspects,
they are treated as separate channels. We assume that the agents have a common ground,
meaning the interface can be understood clearly among them (e.g., all agents use English
and are on-topic).

  - _𝑥𝑐𝑜𝑙𝑙𝑎𝑏_ : the input perceived by the system.

  - _𝑦𝑐𝑜𝑙𝑙𝑎𝑏_ : the system’s output, modeled as _𝑦𝑐𝑜𝑙𝑙𝑎𝑏_ = _𝑆_ (O _𝑐𝑜𝑙𝑙𝑎𝑏,_ E _,𝑥𝑐𝑜𝑙𝑙𝑎𝑏_ |A _,_ C).


Through this structured workflow, agents in an LLM-based MAS can collaborate adaptively,
responding to the task requirements, learning from each other, and coordinating actions to achieve
shared objectives. An example can be seen in [39], where the collaboration channels are predefined through a Directed Acyclic Graph with each edge as agents handling and receiving outputs,
allowing the agents to effectively collaborate towards performing tasks in a simulated Minecraft
game environment. Another instance is illustrated in [67], where the collaboration between agents
is planned first, then the agents are carried out to perform the coding task.
Fig. 2 illustrates the agent and its components, as well as the concept of multi-agent collaboration.
By defining these components, we can better analyze the collaborative mechanisms necessary for
complex, goal-oriented AI collaborations. For instance, a straightforward collaboration mechanism
is majority voting, similar to ensemble learning. Collaboration can occur at different stages: (i)
late-stage collaborations, such as ensembling outputs/actions _𝑦_ towards collaborative goals, (ii)
mid-stage collaborations, for example, exchanging parameters or weights of multiple models _𝑚_
in federated and privacy-preserving manners, and (iii) early-stage collaborations include but not
limited to sharing data, context, and environment for model development.


Multi-Agent Collaboration Mechanisms: A Survey of LLMs 9




















|Environment / Context|Perception|Col3|
|---|---|---|
|**Environment**<br>**/ Context**|**AI Model**|**Adapter**|
|**Environment**<br>**/ Context**|**AI Model**|**...**|
|**Environment**<br>**/ Context**|**AI Model**|**Adapter**|
|**Environment**<br>**/ Context**|**Action**<br>|**Action**<br>|
















|Environment / Context|Perception AI Model Action Adapter ... Adapter AI Agent|Col3|
|---|---|---|
|**Environment**<br>**/ Context**|**Perception**|**Perception**|
|**Environment**<br>**/ Context**|**AI Model**|**Adapter**<br>|
|**Environment**<br>**/ Context**|**AI Model**|**...**|
|**Environment**<br>**/ Context**|**AI Model**|**Adapter**|
|**Environment**<br>**/ Context**|**Action**<br>|**Action**<br>|






























|Environment / Context|Perception|Col3|
|---|---|---|
|**Environment**<br>**/ Context**|**AI Model**<br>|**Adapter**|
|**Environment**<br>**/ Context**|**AI Model**<br>|**...**|
|**Environment**<br>**/ Context**|**AI Model**<br>|**Adapter**|
|**Environment**<br>**/ Context**|**Action**<br>|**Action**<br>|



Fig. 2. Our proposed framework for LLM-based multi-agent collaborative system. Each agent consists of
a language model _𝑚_ as the neural processor, current objective _𝑜_, environment _𝑒_, input perception _𝑥_ and
corresponding output/action _𝑦_ . The framework’s central focus is on collaboration channels C that facilitate
coordination and orchestration among agents. These channels are defined by their actors (agents involved),
type, structure, and strategy. Our framework is flexible, accommodating previous approaches and enabling
the analysis of diverse MASs under a unified structure.


**3.2** **Problem Definition**


In an LLM-powered MAS, it is vital for the agents to collaborate with each other, sharing a common
objective or set of objectives. Each collaboration has a communication channel _𝑐_ . The collaboration
includes 1) delegating agents (two or more) with certain objectives based on their unique expertise
and resources, 2) defining their collaboration mechanisms for working together, and 3) decision
making between agents to reach the final goal.


_𝑦𝑐𝑜𝑙𝑙𝑎𝑏_ = _𝑆_ (O _𝑐𝑜𝑙𝑙𝑎𝑏,_ E _,𝑥𝑐𝑜𝑙𝑙𝑎𝑏_ |A _,_ C) = { _𝑐_ _𝑗_ ({ _𝑎𝑖_ ( _𝑜𝑖,_ E _,𝑥𝑖_ )| _𝑎𝑖,𝑜𝑖,𝑥𝑖_ ∈ _𝑐_ _𝑗_ })| _𝑐_ _𝑗_ ∈C} (1)


where each _𝑐_ _𝑗_ ∈C represents a communication channel facilitating the collaborative actions of
agents _𝑎𝑖_ based on their respective inputs _𝑥𝑖_, and allowing them to work together. Working together
here goes beyond communication (the exchange of information), requiring deeper collaborative
behaviors involving coordination and management, and is key to enabling the capabilities of MASs.
Each collaboration channel serves as the mechanism through which agents work together,
characterized by specific attributes: actors (agents involved), type, structure, and strategy. For
instance, channel types can vary, encompassing competition, cooperation, or coopetition, while
structures can be peer-to-peer, centralized, or distributed. A difference in any attribute results in a
distinct collaboration channel. As an example, in a peer-to-peer structured system, two LLMs may
compete, while others cooperate; these distinct interaction types result in separate collaboration
channels. This flexible channel framework allows agents to adapt their interactions, optimizing
multi-agent collaborative effort and task efficiency across diverse scenarios.


10 Tran et al.


**4** **Methodology**


**4.1** **Overview**


This section provides an extensive review of LLM-based multi-agent collaborative systems, emphasizing their key characteristics, including the mechanisms for coordination and orchestration among
agents - collaboration channels - types, strategies, and structures. Fig. 2 presents our proposed
framework for MASs, detailing their core components and interconnections.
Our survey strategy involves systematically analyzing existing research on MASs to identify the
defining characteristics of multi-agent collaboration. From this analysis, we deduce the fundamental
components and trends in MAS design and synthesize them into a cohesive framework. First, each
LLM-based agent in the system is equipped with an LLM _𝑚_, current objective _𝑜_, environment _𝑒_, input
perception _𝑥_, and corresponding output/action _𝑦_ . This is visualized in the left part of Figure 2 and
described formally using mathematical notations in Section 3.1. Our central focus in this framework
is the collaboration channels C between agents that facilitate coordination and orchestration among
agents. These channels are characterized by their actors (agents involved), type (e.g., cooperation,
competition, or coopetition), structure (e.g., peer-to-peer, centralized, or distributed), and strategy
(e.g., role-based, rule-based, or model-based). Collaboration mechanisms span various levels of
machine learning processes, including data exchange, shared input embeddings, model sharing,
and output sharing, enabling agents to interact effectively and leverage each other’s strengths.
For each component, we discuss the prevailing implementation trends and methodologies observed in the literature. We examine how these methods align with our proposed framework. We
summarize our main findings and lessons learned at the end of the section, offering guidance for
future research in the field.


**4.2** **Collaboration Types**

_4.2.1_ _Cooperation._ Cooperation in LLM-based MASs occurs when agents align their individual
objectives ( _𝑜𝑖_ ) with a shared collective goal (O _𝑐𝑜𝑙𝑙𝑎𝑏_ ), working together to achieve a mutually
beneficial outcome: O _𝑐𝑜𝑙𝑙𝑎𝑏_ = [�] _𝑖_ _[𝑛]_ =1 _[𝑜][𝑖]_ [. Agents assess each other’s needs and capabilities, actively]
seeking collaborative opportunities. Moreover, agents can also be utilized to focus on specific
sub-tasks within their expertise, enhancing efficiency and reducing completion times [24]. This
type of collaboration is essential in tasks where collaborative problem-solving, collective decision
making, and complementary skill sets contribute to achieving complex objectives that a single
agent could not complete as effectively [26, 29, 33].
Several research papers highlight the importance of cooperation in LLM-based MASs. For instance, in [117], a feedback loop is carried out as the main collaboration channel, where the task
is first handled by an LLM model (Actor), then an Evaluator and Self-Reflection model rates the
output and results, producing verbal guidance for the Actor to improve. In Theory of Mind for
Multi-Agent Collaboration [75], agents gain a shared belief state representation within the environment E, helping them track each other’s goals and actions, thereby facilitating smoother
coordination and better collaborative outcomes. This shared state has led to emergent collaborative
behaviors and high-order Theory of Mind capabilities in LLM agents, though challenges remain
in optimizing long-horizon planning and managing hallucinations. In AgentVerse [24], agents
specialize in distinct roles, such as recruitment, decision-making, or evaluation, within a cooperative framework, which improves system efficiency by leveraging each agent’s unique expertise.
Similarly, MetaGPT [56] uses an assembly line model, assigning roles and encoding Standardised
Operating Procedures (SOPs) into prompts _𝑟𝑖_ to enhance structured coordination and produce
modular outputs _𝑦𝑖_ . MetaGPT underscores the potential of integrating human domain knowledge
into MASs. Cooperative approaches have shown success in areas like question answering [54],


Multi-Agent Collaboration Mechanisms: A Survey of LLMs 11


Table 2. Collaboration types: definitions, advantages, disadvantages, and example scenarios.


**Type** **Definition** **Advantages** **Disadavantages** **Example Scenario** **Refs.**


Cooperation Agents align their  - Assigns sub-tasks to  - Misaligned goals can Code generation [12, 56, 60, 117]
objectives and work agents based on strengths. cause inefficiencies. Decision making [91, 117]
together toward a         - Simple to design and         - One agent’s failure Game environments [75]
shared goal. execute with clear goals. can be amplified. Question answering [33, 54, 74, 117]
Recommendation [131]
Competition Agents prioritize  - Pushes agents to perform  - Needs mechanisms Debate [77]
their own objectives, better. to resolve conflicts. Game environments [22, 155]
which may conflict         - Promotes adaptive         - Ensures competition Question answering [54, 104]
with others. strategies. is beneficial.
Coopetition A blend of  - Balances trade-offs to  - Few studies explore Negotiation [2, 34]
cooperation and reach mutual agreements. coopetition in depth.
competition where
agents collaborate
on shared tasks
while competing
on others.



i



i



i



i



i



i



i



i



i


Fig. 3. Illustrative examples of collaboration types, where each agent _𝑎_ is equipped with different tools or
capabilities through their system prompt _𝑟_ . In scenario a), agents cooperate by leveraging their individual
specialties (e.g., writing, translation, research) to achieve a shared goal (academic writing). In scenario b),
agents compete and debate against each other fo r their own goals. In scenario (c) of coopetition, agents
compromise with each other, compete on one aspect while agreeing on another.


recommendation systems [131], and collaborative programming [60], where agents cooperate
together with specialized roles, such as manager, searcher, or analyst, to achieve complex goals.
There are recent open-source frameworks allowing for experimentation with cooperative LLMbased MASs. CAMEL [74] provides a role-playing framework where a task-specific agent and two
cooperating AI agents (User and Assistant) work to complete tasks via role-based conversations.
Similarly, AutoGen [134] enables developers to define flexible agent behaviors and communication
patterns, allowing LLM agents to cooperate through conversation and tackle complex tasks by
decomposing them into manageable subtasks.
However, cooperation in MASs also presents challenges. Frequent communication and multiple
collaboration channels in C between agents can lead to increased computational cost and complexity.
Coordinating actions between multiple agents, particularly in dynamic environments, can also be
difficult without well-defined collaboration channels _𝑐𝑖_ . Although cooperation is the primary goal,
conflicts may arise if agents interpret shared objectives differently or if situations require dynamic
adaptation. For example, in the book marketplace application described in [91], agents may act
unpredictably by sending messages to themselves, pretending to be clients. The overall success of a


12 Tran et al.


cooperative MAS is also dependent on the reliability and performance of individual agents, as the
failure of one agent or more agents (e.g., infinite conversation loop, amplified hallucinations [56])
can negatively impact the entire system. Therefore, mechanisms such as failure handling and
trustworthiness need to be considered.


_4.2.2_ _Competition._ Competition happens when there are conflicting objectives or scenarios of
limited resources. In this type of interaction, agents prioritize their individual goals ( _𝑜𝑖_ ), which may
clash with or oppose the objectives of others, introducing an element of rivalry: O _𝑐𝑜𝑙𝑙𝑎𝑏_ = { _𝑜𝑖_ | _𝑜𝑖_ ≠
_𝑜_ _𝑗,_ ∀ _𝑖_ ≠ _𝑗_ }. However, this competition can still orient toward the collective goal _𝑂𝑐𝑜𝑙𝑙𝑎𝑏_, such as in
the scenario of debate. In LLM-based MASs, competitive dynamics can emerge in tasks such as
debate, or strategic gameplay, where agents seek to maximize their own success criteria [22, 155].
Incorporating competition into collaborative MASs can enable innovation and improve the
robustness of agents’ responses. Competition encourages agents to develop advanced reasoning
and more creative problem-solving and strengthens the system’s adaptability by testing the limits of
each agent’s capabilities. In frameworks like LLMARENA [22], LLM-based MASs with competition
as the main collaboration type, are benchmarked across seven dynamic gaming environments. For
instance, in the game TicTacToe, the board is represented textually within the environment E, and
two LLM agents are instructed (through their system prompts _𝑟𝑖_ ) compete, aiming to out-maneuver
each other since their individual goals _𝑜𝑖_ are mutually exclusive. Crucially, the authors highlight
that competition between LLM agents enables skills such as spatial reasoning, strategic planning,
numerical reasoning, risk assessment, communication, opponent modeling, and team collaboration. However, they also acknowledge that LLMs still have a significant journey ahead in their
development towards becoming fully autonomous agents, especially in opponent modeling and
team collaboration, due to their intrinsic limited capability to interact with other actors. A game
environment is also simulated in [155], where 2 agents act as two restaurant managers competing
for 50 customers. Carefully designed prompts _𝑟_ set the scenario, contextualizing the agents’ environment (E) and providing a comprehensive restaurant management system accessible through
APIs (external tools). Each agent’s context _𝑒𝑖_ includes information about the rival’s performance
from the previous day, including the menu, number of customers, and feedback. In this scenario,
the collaboration channel _𝑐_ between the two managers is competitive, illustrating how structured
competition drives agents to refine strategies, conforming to several classic sociological and economic theories. Similarly, in LEGO [54], a multi-agent collaborative framework is introduced for
causality explanation generation, where the competition collaborative link _𝑐_ is also pre-defined.
The collaboration consists of 2 LLMs, one serves as Explainer with initial output, and another one
acts as Critic, with iterative refinement and feedback. In [104], the collaboration between LLM
agents happens at an earlier stage during training, where multiple expert agents are combined and
trained together through an objective that lets the agents compete for the best candidate answer
and identifying agents trained on the domain of the input question.
The competitive approach offers advantages such as promoting robustness, strategic adaptability,
and complex problem-solving capabilities within MASs. However, competition can also introduce
challenges, including potential conflicts that require mechanisms to ensure that competition remains
constructive and beneficial to overall system goals. Effective coordination efforts between agents
are important, especially for competition collaboration type. As studied in [128], a MAS approach
with suboptimal design for their competitive collaboration channels can be overtaken by singleagent counterparts with strong prompts (including relevant few-shot demonstrations) on a range of
reasoning tasks and backbone LLMs. In settings where cooperation is desired, excessive competition
may hamper alignment, requiring frameworks to balance these aspects effectively.


Multi-Agent Collaboration Mechanisms: A Survey of LLMs 13


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
