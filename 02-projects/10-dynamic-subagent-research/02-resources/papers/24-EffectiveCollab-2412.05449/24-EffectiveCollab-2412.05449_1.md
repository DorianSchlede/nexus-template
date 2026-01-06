<!-- Source: 24-EffectiveCollab-2412.05449.pdf | Chunk 1/4 -->

## **Towards Effective GenAI Multi-Agent Collaboration:** **Design and Evaluation for Enterprise Applications**

**Raphael Shu** _[∗]_ **, Nilaksh Das** _[∗]_ **, Michelle Yuan** _[∗]_ **, Monica Sunkara, Yi Zhang**
AWS Bedrock


**Abstract**


AI agents powered by large language models (LLMs) have shown strong capabilities in problem solving. Through combining many intelligent agents, multi-agent
collaboration has emerged as a promising approach to tackle complex, multi-faceted
problems that exceed the capabilities of single AI agents. However, designing the
collaboration protocols and evaluating the effectiveness of these systems remains a
significant challenge, especially for enterprise applications. This report addresses
these challenges by presenting a comprehensive evaluation of coordination and
routing capabilities in a novel multi-agent collaboration framework. We evaluate
two key operational modes: (1) a coordination mode enabling complex task completion through parallel communication and payload referencing, and (2) a routing
mode for efficient message forwarding between agents. We benchmark on a set of
handcrafted scenarios from three enterprise domains, which are publicly released
with the report. For coordination capabilities, we demonstrate the effectiveness of
inter-agent communication and payload referencing mechanisms, achieving end-toend goal success rates of 90%. Our analysis yields several key findings: multi-agent
collaboration enhances goal success rates by up to 70% compared to single-agent
approaches in our benchmarks; payload referencing improves performance on
code-intensive tasks by 23%; latency can be substantially reduced with a routing
mechanism that selectively bypasses agent orchestration. These findings offer
valuable guidance for enterprise deployments of multi-agent systems and advance
the development of scalable, efficient multi-agent collaboration frameworks.


**1** **Introduction**


The rapid advancement of AI agents driven by large language models (LLMs) [3] has opened
new frontiers towards solving complex problems. Based on the strong reasoning and tool-use
capabilities, an agent can plan and execute multiple steps for actions until the goal of problem solving
is reached [23]. However, as the complexity of real-world challenges continues to grow, there is an
increasing need for scaling up the agent-based systems by coordinating with multiple agents with
diverse specializations [17].


Towards tackling multi-faceted real-world problems, _multi-agent system (MAS)_ research emerged in
the mid-1980s to early-1990s as a critical sub-field of artificial intelligence focused on developing
computational systems composed of multiple interacting intelligent agents [18]. Researchers sought
to create frameworks where autonomous entities could communicate, coordinate, and solve problems
collectively [20]. With the rise of LLM-based AI agents in recent years, the key challenges in MAS
research regained focal attention in the new Generative AI (GenAI) era [8]. While earlier MAS work
drew inspirations heavily from fields like distributed computing and game theory, new LLM-based
GenAI agent research looks further into inter-disciplinary influence from psychology and social
science as the AI agents start to demonstrate human-like intelligence as well as social behavior [16].


_∗_ Authors contributed equally


Figure 1: Illustration of the hierarchical agents approach for multi-agent collaboration. In a centralized
hierarchy, a supervisor agent oversees and assigns tasks to specialist agents. The figure demonstrates
a multi-layer hierarchy, where an agent can function as both a specialist agent and a supervisor agent.


One particularly fruitful research avenue in GenAI MAS research is the exploration of _multi-agent_
_collaboration (MAC)_ [9]. Operating under the “collaborative assumption” [13] – a premise that agents
are fundamentally motivated to achieve shared or compatible goals and prioritize collective problem
solving over individual self-interest – multi-agent collaboration aims to address the key challenges
such as communication protocols, goal alignment, group decision-making, scalability, and trust and
reliability [4, 21, 25]. In this paper, we present a particular design of MAC framework targeting
the development of MAC applications for real-world enterprise use cases. Three research questions
arise for having multiple LLM-based agents to work together: 1) how to define the collaboration
mechanism, 2) how to facilitate efficient knowledge exchange between agents, and 3) how to evaluate
the effectiveness and efficiency of collaboration. In this technical report, we propose strategies to
address these research questions. Based on collected evaluation datasets, we report the evaluation
results and detailed analysis on the effectiveness and efficiency of multi-agent collaboration.


**Collaboration Mechanism** Collaboration mechanisms define how agents interact with each other
to achieve a common goal [24]. Two key aspects are important: team hierarchy and decision-making
mechanisms. Both hierarchy and decision-making can be either centralized or decentralized [7].
In a centralized hierarchy, a central authority assigns or delegates tasks to agents, whereas in a
decentralized hierarchy, agents take their own initiatives. On the other hand, centralized decisionmaking involves a single agent making the final decision, while decentralized decision-making often
relies on consensus or voting among multiple agents.


The literature presents various approaches to these mechanisms. For example, ChatDev [17] employs
a centralized team hierarchy and decision-making mechanism, while MAD [19] and Generative
Agents [16] adopt decentralized hierarchies and decision-making processes.


In MAC, we start by exploring centralized approaches which we refer to as hierarchical agents, and
expand to decentralized mechanisms as future work. In hierarchical agents, each team has a tree-like
hierarchy, with the root agent responsible for the the team goal and the "leaf" agents responsible
for sub-tasks. We refer to the root agent as supervisor Agent. The supervisor Agent is required to
perform task planning, break down the task, assign sub-tasks, and facilitate communication between
specialist agents.


As shown in Figure 1, such a hierarchy can extend to multiple levels, with leaf agents acting as
supervisors for other specialist agents. This hierarchical approach allows each leaf agent to focus on
their specialized tasks, while the Supervisor Agent manages planning, delegation, and coordination.
Unlike building a monolithic agent capable of solving a wide range of tasks, this approach enables
the LLM behind each agent to maintain a limited context relevant to their specific role. Additionally,
developing and benchmarking specialist agents becomes more manageable, and the development


2


process can be distributed across multiple agent developers. Note that although the supervisor agent
can delegate tasks to other agents, it is still the responsibility of the supervisor agent to complete the
task and bring the results back to the user.


**Inter-Agent Knowledge Exchange** Knowledge exchange between agents is a fundamental aspect
of multi-agent collaboration. In this technical report, we focus on enabling the most basic form of
knowledge exchange: message passing. Each agent can send direct messages to other visible agents.
Within the context of hierarchical agents, an agent can send and receive messages from its supervisor
and, potentially, from specialist agents. We initially support synchronized communication, where
message passing temporarily blocks the execution of the sender agent until a response is received.
This protocol can be extended to support asynchronous communication, allowing the sender agent to
continue execution while waiting for a response.


**Multi-Agent Evaluation** Benchmarking single AI agents is already difficult [10] and increasing
the number of agents to benchmark only complicates the problem. While an ideal approach is to
have a human try out the multi-agent system and evaluate whether every conversation is successful or
not, this kind of online evaluation is too expensive and not scalable for fast prototyping. To rapidly
evaluate our multi-agent systems, we introduce assertion-based benchmarking as a way to leverage
model-based evaluation and avoid dependency on collecting ground-truth conversation trajectories.
For assertion-based benchmarking, we collect 90 scenarios from three different enterprise application
domains. We open-source the benchmarking dataset and conversation evaluation script. [2]


For enterprise applications, efficient collaboration is crucial, as many are latency-sensitive. To address
this, we further optimize the multi-agent collaboration framework by introducing payload referencing
and a dynamic routing mechanism. The remainder of this report provides details on methodologies
and optimizations in Section 3. Evaluation results and analysis are presented in Sections 4 to 6.
Finally, we discuss limitations and future work in Sections 7 to 8.


**2** **Related Work**


**Multi-agent GenAI Systems** An agent is defined as “an entity which is placed in an environment and senses different parameters that are used to make a decision based on the goal of the
entity.” [10]. The motivation for multi-agent systems is to have agents collaborate on a complex
task that could not have been accomplished by a single agent. With the rise of LLMs, researchers
have proposed leveraging the reasoning and planning capabilities of these models to develop more
sophisticated multi-agent systems. Examples of such multi-agent LLM systems include MetaGPT [9]
and CAMEL [12]. MetaGPT is one of the first multi-agent LLM projects that tries to mimic a
software company. Developers can provide a standard operating procedure and MetaGPT tries to
assign roles to various agents. CAMEL, or Communicative Agent Framework, promotes independent
collaboration between LLM agents. Its key innovation is the use of "inception prompting," a method
that steers conversational agents to complete tasks. Beyond its practical applications, CAMEL also
functions as a research platform. It enables the creation and analysis of conversational data, offering
valuable insights into the behavior and interactions of communicative agents. Across these works,
much of the emphasis is on customization and coordination, which was much less prominent in
traditional multi-agent systems [18, 20].


**Multi-agent Frameworks and Platforms** CrewAI [5] is designed to enhance task execution
by organizing agents into specialized roles, similar to team members in a crew. This approach
emphasizes task decomposition, where a complex problem is broken down into smaller, manageable
subtasks. Each agent is assigned a specific role based on its expertise, allowing for efficient problemsolving. AutoGen [22] represents a significant advancement in enabling multi-agent systems to
engage in sophisticated conversations. This framework allows agents to communicate and collaborate
by sharing information and refining their outputs through iterative interactions. By simulating
human-like dialogues, AutoGen enables agents to negotiate, plan, and execute tasks collaboratively.


LangGraph [11] introduces an innovative framework for organizing agent interactions using directed
acyclic graphs (DAGs). This structure allows for clear visualization and management of dependencies


2 `[https://github.com/aws-samples/multiagent-collab-scenario-benchmark](https://github.com/aws-samples/multiagent-collab-scenario-benchmark)`


3


between tasks and agents. By leveraging DAGs, LangGraph optimizes the flow of information and
decision-making processes among agents. This approach enhances the system’s ability to handle
complex, interdependent tasks by ensuring that each agent’s actions are informed by the outcomes of
preceding steps.


**End-to-end Agent Evaluation Frameworks** While our work on assertion-based benchmarking is
ongoing, there are other works in the literature that are similar. AgentEval [2] has a multi-agent setup
where there are three agents to evaluate conversation trajectories: 1) CriticAgent, 2) QuantifierAgent,
3) VerifierAgent. The CriticAgent takes the task description as input and outputs a list of criteria for
task success. The QuantifierAgent then assesses whether the trajectories meet the criteria and the
outputs here can be a scalar value. The VerifierAgent will finally verify that the evaluation is accurate
and complete. Note that the criteria proposed by the CriticAgent is much more coarse-grained like
“clarity” and “efficiency”.


AgentQuest [6] proposes to measure success with a “progress rate” that is based on a set of milestones.
The progress rate measures how many milestones are completed and milestones are defined to be
“environment hidden states the agent needs to reach to get the final solution of the task”. AgentQuest
focuses benchmarking agents for game-like datasets like ALFWorld and Sudoku, so state naturally
comes with the environment when the agent plays the game. These milestones can either be externally
annotated or programmatically defined within the simulation.


Most recently, ToolSandbox [14] is the work in literature most similar to our evaluation setup. ToolSandbox also includes a user simulator and environment executor for tools. Before the simulations,
they also pre-define “milestones” and “minefields” for each session. Milestones are events that must
occur during the conversation and minefields are those that should not happen. These milestones
and minefields are similar to our assertions that cover actions and agent behaviors. In addition, their
implementation stores an “Execution Context” that contains the “world state” to mimic tasks that
manipulate a resource like a database.


**3** **Modeling**


Multi-agent collaboration enables developers to combine specialized agents to solve complex problems. Each agent can be independently developed, optimized, and configured to leverage its unique
strengths. Compared to single-agent workflows, multi-agent collaboration integrates the complementary capabilities and expertise of agents with different specializations, making it highly effective for
addressing complex tasks. Developers can achieve amplified capability, flexibility, and scalability
by deploying a team of agents. Moreover, multi-agent solutions can have higher robustness and
fault tolerance by using redundant agents in the team. For complex tasks, multi-agent solutions can
improve efficiency by distributing the tasks to multiple agents and parallelizing the execution.


From a developer experience perspective, the development process is simplified by dividing functionalities among multiple agents. Developers can potentially reuse and compose existing agents
for different multi-agent solutions. In some cases, cost-effective solutions can be built by utilizing
low-cost orchestrating LLMs for specific agents. In this section, we review the primary features of
MAC, which include inter-agent communication, payload referencing, and dynamic agent routing.


**3.1** **Inter-Agent Communication**


We model the inter-agent communication capability as a specialized tool that can be leveraged by the
supervisor agent. This approach allows us to seamlessly extend the agents’ communication abilities
by integrating it with the existing function calling capability. The key aspects of this approach are:


1. **Unified Communication Interface:** The user is treated as another agent in the system,
allowing for a consistent communication interface across all interactions — whether it’s
between the user and supervisor agent, or between the supervisor agent and specialist agents.

2. **Parallel Communication:** The supervisor agent can engage in parallel communication with
multiple specialist agents simultaneously, enabling more efficient task completion through
concurrent information exchange (Figure 2).

3. **Leveraging Existing Function Calling Capability:** By modeling communication as a tool,
the supervisor agent can utilize the same underlying mechanisms for function calling to


4


Figure 2: Example of parallel agent communication. In this example, the supervisor agent simultaneously communicates with multiple agents as the tasks can be completed independently.


facilitate inter-agent messaging. This ensures a cohesive integration with the foundational
model’s existing tool-use capabilities.


We provide the supervisor agent with a tool called `send_message`, which has two parameters:
`recipient` and `content` . This tool allows the supervisor agent to send messages to other agents.
Additionally, the incoming messages from specialist agents are tagged in the following format:

```
<message from="$SOURCE_AGENT">
...
</message>

```

Overall, this approach to inter-agent communication helps to create a more unified and extensible
multi-agent collaboration framework.


**3.2** **Payload Referencing**


Payload referencing is a specialized mechanism designed to handle the exchange of large content
blocks, particularly code snippets (Figure 3). This mechanism aims to reduce the latency of the supervisor agent by allowing direct injection of text extracted from past multi-party communication into the
message content. This is an important optimization for inter-agent communication, as the supervisor
agent often needs to provide relevant context from previous interactions when communicating with
specialist agents.


For example, let’s say the supervisor agent (Agent A) needs to ask a specialist agent (Agent B) to
perform a specific task based on the output of another specialist agent (Agent C). Instead of having
Agent A regenerate the full context and details of the message from Agent C, the payload referencing
mechanism allows Agent A to simply reference the relevant text from its past interactions. This can
significantly reduce the number of output tokens required in the message to Agent B, leading to faster
communication and reduced latency.


When a specialist agent generates a message containing structured content (e.g., code blocks), the
system automatically detects these sections. For each incoming message to the supervisor agent,
the detected content blocks, referred to as payloads, are assigned unique identifiers and wrapped
with special tags that include these identifiers before being sent to the supervisor agent. Instead of
repeatedly regenerating large static payloads in its outgoing messages to other specialist agents, the
supervisor agent is instructed to reference previously detected payloads using the assigned identifiers.
This allows the supervisor agent to use a simplified reference tag when sending messages. For every
outgoing message from the supervisor agent, the system detects these reference tags and replaces


5


Figure 3: Example of payload referencing mechanism. In this example, the Coder agent delivers code
which is then detected and tagged. The supervisor agent can then use the tag as a reference which
would then be expanded to the original content for the Test agent.


Figure 4: Dynamic agent routing, where an incoming request can be routed directly to a specialist
agent, with their messages relayed back to the user.


them with the corresponding payloads before sending them to the other specialist agents. This
technique enables the supervisor agent to reference payloads by generating a significantly reduced
number of tokens compared to generating the entire payload itself.


Our ablation experiments with the payload referencing capability demonstrated a 27% relative
reduction in the average communication overhead per turn of the supervisor agent. This is discussed
in more detail in Section 6.1.


**3.3** **Dynamic Agent Routing**


Given a complex problem, a supervisor agent often needs to communicate with multiple specialist
agents across several rounds to complete the task. However, when the incoming request is simple and
relevant to only a single specialized agent, triggering the full coordination capability of the supervisor
agent introduces unnecessary overhead, slowing down the collaboration. In such cases, the supervisor


6


agent only needs to route the incoming message to the appropriate specialist agent, avoiding the
inefficiency of the full orchestration process.


To address this communication overhead, we introduce a dynamic agent routing mechanism that
selectively bypasses the supervisor agent’s orchestration when the incoming message only requires
simple routing, such as the example shown in Figure 4. The routing decision is made using a fast
classifier that predicts whether the incoming message can be directly routed without additional
processing. If the classifier is uncertain, it can still trigger the full orchestration process as a fallback.
Note that the supervisor agent is always aware of the routing actions, and the communication between
the requester and specialist agents will be available in the agent memory even the orchestration
process is bypassed.


Applying dynamic agent routing can substantially improve the efficiency of multi-agent collaboration,
particularly for latency-sensitive use cases. However, the success of dynamic agent routing relies on
an accurate classifier capable of determining when a request requires the supervisor agent’s processing
with low latency. In our experiments, we demonstrate that this classification step can achieve _≥_ 90%
accuracy with a latency of approximately 350 ms.


**4** **End-to-end Automatic Evaluation**


Recent literature have noted the challenges associated with LLM agents benchmarking, which are
often due to the dynamic and complex nature of the problem. The definition of success is often
unclear as it can refer to either from the user perspective or from the environment/system, as users
may not fully know what happens “behind-the-scenes”. Moreover, benchmarks may not consider
that user feedback can help agents achieve their goals. If the user is not properly simulated, then the
evaluation undermines the agent’s capability to orchestrate tasks with a human in the loop.


Prior single-agent benchmarking is more static where user inputs and follow-up responses are predefined before evaluation. The gold-truth actions would be collected along with the conversations,
which would then be compared to the actions generated by the agent. This static setup already has
some issues because it assumes that the user goals can only be fulfilled through executing a certain set
of actions. In reality, there may be multiple trajectories that enable the agent to fulfill user requests.
If those trajectories are not captured in the gold-truth, then the agent is incorrectly penalized.


To generalize evaluation metrics for agents, we formally define the success of agent for a given
user _u_ and scenario _s_ as _Xu_ _[s]_ [, a Bernoulli random variable that represents success or failure for the]
user-agent session. A scenario is defined as the setting for a session which includes user goals and
task domain. Since user profiles and scenarios vary, we are interested in the expected value of success
for any user-agent session:


E _U,S_ [ _Xu_ _[s]_ [] =] _[ p]_ [success] (1)


where _p_ success is the success rate of an agent with a sampled user from user pool _U_ and scenario
sampled from collection _S_ . The objective of benchmarking is to approximate _p_ success.


We can easily extend this formulation to multi-agent systems. However, with more agents added, the
complexity grows and _p_ success is more difficult to approximate. Several, different trajectories could be
considered correct and sometimes no actions need to be executed to achieve user goals. We propose
**assertion-based benchmarking** as a way to better approximate likelihood of agent success.


The assertion-based evaluation framework relies on three components: 1) benchmarking data collection, 2) environment simulators, 3) automatic assertion judge (Figure 5). First, a set of scenarios
need to be collected according to pre-defined agent profiles and tool schemas for a particular domain.
With each scenario, a list of assertions needs to be included. These assertions are statements that
must hold true for a conversation to be considered successful. This is similar to debugging software
with test cases. Second, the user simulator is initialized from the scenario and input problem and
begins to interact with the multi-agent system. An action simulator is also used to simulate the tool
calls from the multi-agent system. The trajectories are recorded for further evaluation. Finally, a
judge determines the validity of each assertion. Based on the number of correct assertions, goal
success rates can be computed to help measure the success of the multi-agent system. In the following
subsections, we cover each component of the framework in depth.


7


Figure 5: Overview of end-to-end assertion-based benchmarking with scenarios and assertions


**4.1** **Benchmarking Data**


There are three artifacts that need to be collected for each scenario. First, the scenario description
itself must list the user goals and any background information. The information in the scenario
description is critical because the user simulator will be grounded on the description. Then, the
second artifact is the input problem, which is the first turn of the conversation from the user. The
input problem will begin the benchmarking simulation.


The final artifact is a list of assertions that need to be satisfied during the simulation. Assertions
are categorized two types: user-side and system-side. User-side assertions cover behaviors of the
multi-agent system that can be observed by the user. On the other hand, system-side assertions cover
behaviors of the multi-agent system that cannot be observed by the user. These assertions may include
tool calling correctness, parameter correctness, inter-agent behavior, or rule compliance. Appendix A
shows example artifacts from our publicly released benchmarking data collection.


**4.2** **Simulation**


For each session, we feed the scenario description and the input problem to a user simulator. The user
simulator is a LLM that is prompted to follow the scenario description. The simulation begins with
the input problem as the first turn of the session. The input problem is delivered to the supervisor
agent who then begins to work the specialist agents. If the specialist agents need to invoke an action,
the function calls are passed to the action simulator, which is a LLM grounded on the provided
tool schemas. The action simulator also has access to past tool invocations so that it can generate
results that is aligned to past observations. After the action simulator returns the simulated action, the
specialist agents continue to carry out the task.


During the simulation, the user simulator will continue to interact with the supervisor agents. The user
simulator can either help clarify any questions from the supervisor agent or keep sending new task
requests. Any requests or answers given by the user simulator should be aligned with the information
in the scenario. Once the user simulator determines that all the goals in the scenario are met, the user
simulator generates a `</stop>` token to end the simulation. Otherwise, we set a maximum number
of user simulation turns to 5 to prevent simulations that fail to end.


**4.3** **Assertion Judgements**


After simulations are completed, we pass the trajectories to a LLM judge to help automate the
assertion evaluation. Along with the simulation trajectories, we also pass the scenario and the
assertions to the judge. The judge returns whether each assertion is True or False, and includes the
reason for their judgement. The reason often exhibits evidence from the conversation, which can


8


Table 1: Definitions of Success Metrics


Metric Definition Implementation


Overall GSR Overall goal success rate covering both Use LLM to judge user-side and systemthe user-side and the system-side side assertions. For a conversation, score
is 1 if all assertions are True; else 0.



Supervisor Goal success rate of the supervisor agent
GSR without any dependence on sub-agent
and tool behavior



If overall GSR is 1 or supervisor agent
is reliable (see reliability metrics), then
score for the conversation is 1; else 0.



User-side GSR Goal success rate in the perspective of Use LLM to judge user-side assertions.
the user For a conversation, score is 1 if all userside assertions are True; else 0.


System-side Goal success rate in the perspective of Use LLM to judge system-side asserGSR the system developers tions. For a conversation, score is 1 if all
system-side assertions are True; else 0.


Table 2: Definitions of Latency Metrics


Metric Definition


Avg. communication Average number of seconds that the supervisor agent spends communioverhead per turn cating with other agents before getting back to the user. This time does
not take into account the duration of agents other than the supervisor
agent.
