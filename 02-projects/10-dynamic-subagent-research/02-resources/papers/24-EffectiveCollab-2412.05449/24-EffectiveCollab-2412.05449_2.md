<!-- Source: 24-EffectiveCollab-2412.05449.pdf | Chunk 2/4 -->



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


Avg. latency per com- Average number of seconds that the supervisor agent spends to deliver
munication each message to communicate with other agents.


Avg. user-perceived Average number of seconds it takes for the supervisor agent to get back
turn latency per session to the user. This time does take into account the duration of all agents in
the system.


Avg. communications Average count of messages sent by the supervisor agent over the entire
per session session.


Avg. output tokens per Average number of total output tokens from the supervisor agent for
communication each message.


easily show why the assertion has succeeded or failed. This is important as multi-agent conversations
can be very lengthy and difficult for people to pinpoint the causes of failures.


**4.4** **Metrics**


A conversation is considered overall successful if all assertions, both user-side and system-side, are
True. We then measure **Goal Success Rate (GSR)** as the percentage of conversations that have all
assertions evaluated as True. This overall GSR is our primary measure of success. We also compute
User GSR and System GSR, which are the variants of GSR where the assertions being evaluated are
limited to one type (either user-side or system-side). These metrics are useful to understand whether
multi-agent systems are failing from the perspective of the user or the system (Table 1).


Beyond goal success, latency is a critical metric in multi-agent systems. As these systems involve
multiple agents interacting and collaborating to perform complex tasks, the time delay between agent
communications and actions can significantly impact user experience. Minimizing latency is crucial
for ensuring the system can operate efficiently, especially in time-sensitive applications. Table 2 lists
the various latency metrics that are included in this report.


Lastly, we also included metrics to evaluate routing mode. For routing mode, we are concerned with
routing classification accuracy, false agent switch rates, turn-level routing overhead, and routing
classification latency (Table 3).


9


Table 3: Definitions of Routing Metrics


Metric Definition


Classification Accuracy Accuracy of routing decisions, calculated based on human annotated ground-truth labels.


False Agent Switch Rate Ratio of routing decisions causing the handling agent to be
switched to a wrong agent


Turn-level Routing Overhead Time taken in the primary agent (including routing classification
(ms) and orchestration) within a user turn.


Classification Latency (ms) Time taken for classifying a single routing decision.


Table 4: Dataset statistics, including average number of goals per scenario, average number of
assertions per scenario, total number of action groups, and total number of APIs/tools.


Dataset Avg. Goals per Scenario Avg. Assertions per Scenario Action Groups APIs/Tools


Travel 2.13 4.55 11 52
Mortgage 1.91 3.99 10 35
Software 1.69 7.47 2 4


**5** **Experimental Results**


To understand how MAC performs for enterprise usage, we choose three business domains to
experiment with. For each domain, we set up a set of agents and tools. Then, we manually collect
benchmarking data for each domain. In this report, we show experiments on thirty scenarios from
each domain. This dataset is also publicly released for others to benchmark their own multi-agent
systems (Section 1). The three domains are as follows:


1. Travel planning: agents help user plan a trip, which includes booking flights, booking hotels,
finding local events, getting information about the weather, etc.

2. Mortgage financing: agents help user with mortgage issues, e.g., submitting loan applications, querying information about properties, retrieving banking information, etc.

3. Software development: agents help user design, implement, test, review, and/or deploy code.


The first two domains are conversational, whereas the third domain is more about automation and
requires minimal interaction with user. For the agent profile design, we have made sure to cover the
following conditions to showcase adoption of multi-agent collaboration for various developer setups:


1. Supervisor agents with and without tools: The supervisor agent for Mortgage has access to
MortgageLoans tools, whereas the supervisor agents for other domains do not have tools.

2. Specialist agents with and without tools: Many specialist agents have their own set of tools.
However, some specialist agents in Software do not have tools as they should have the
capability to complete the tasks without them.

3. Agent hierarchy with depth more than one: In Software, the supervisor agent can call on
Deploy agent, which can then call on Infrastructure agent and Application agent.


Table 4 shows an overview of the statistics for the three datasets. Action groups refer to group of
tools (e.g. “BookFlight” action group is a set of tools for searching flights, booking flights, getting
flight details, etc.). Travel and Mortgage each have more than thirty tools, whereas Software has only
two tools. Software tends to have more assertions on average than Travel and Mortgage. Appendix B
shows the agents for each domain and their associated action groups, which are the set of tools that
the agents have access to.


**5.1** **Coordination Mode Experiments**


We report the goal success metrics for coordination mode across a variety of settings in Table 5.
For evaluating the assertions, we leverage OpenAI’s GPT-4o model [15] for providing LLM-based


10


Table 5: End-to-end evaluation of Coordination Mode


Setting Dataset Overall GSR Supervisor GSR



Supervisor: Sonnet 3.5 (20241022)
Specialists: Sonnet 3.5 (20241022)


Supervisor: Sonnet 3.5 (20241022)
Specialists: Sonnet 3.0


Supervisor: Sonnet 3.5 (20241022)
Specialists: Haiku 3.5



Travel 0.90 0.90
Mortgage 0.90 0.93
Software 0.90 1.00


Travel 0.87 0.90
Mortgage 0.90 0.97
Software 0.77 0.90


Travel 0.80 0.87
Mortgage 0.83 0.90
Software 0.87 0.93



Travel 0.60                    Single-agent: Sonnet 3.5 (20241022) Mortgage 0.80 Software 0.53                   

Table 6: Latency Performance of Coordination Mode



Avg. communication
Setting Dataset overhead per turn (s)



Avg. user-perceived
turn latency
per session (s)



Supervisor: Sonnet 3.5 (20241022)
Specialists: Sonnet 3.5 (20241022)


Supervisor: Sonnet 3.5 (20241022)
Specialists: Sonnet 3.0


Supervisor: Sonnet 3.5 (20241022)
Specialists: Haiku 3.5



Travel 13.75 31.46
Mortgage 13.39 24.42
Software 35.44 168.73


Travel 15.43 42.12
Mortgage 15.97 29.90
Software 53.48 137.31


Travel 12.95 23.98
Mortgage 11.03 18.13
Software 36.65 125.31



Travel                       - 14.12
Single-agent: Sonnet 3.5 (20241022) Mortgage    - 9.12
Software                      - 52.61


judgements. The results demonstrate that multi-agent collaboration achieves the best overall GSR
of 90% across the three evaluated domains when the Claude 3.5 Sonnet (20241022) model [1] is
utilized as both the supervisor agent and the specialist agents.


We further examine the impact of using different agent models. Switching the specialist agent model
from Claude 3.5 Sonnet to Claude 3.0 Sonnet shows a significant regression in the performance for
the Software development domain. This is also apparent when the specialist agent is switched to
Claude 3.5 Haiku, as the performance in the Software domain is mostly recovered with this newer
generation of models.


We also compare the performance of a single agent with the multi-agent collaboration approach. In
this experiment, a single agent is given the tools from all specialist agents combined and is responsible
for assisting the user. We reuse the assertions collected for the multi-agent setup but replace any
mentions of specialist agents with supervisor agent (e.g. “flight agent books tickets” becomes “travel
agent books tickets”). For any assertions about inter-agent behaviors, we would replace mentions
of the primary agent with “user” and mentions of the specialist agent with the supervisor agent
(e.g. “code agent implements code and delivers back to software agent” becomes “software agent
implements code and delivers back to user”).


In the single-agent setting, we observe an absolute regression of up to 37%. MAC allows each
specialist agent to be provided with instructions for the specific subset of tasks it is supposed to
handle. This specialized task assignment may not be achievable by a single agent, which may struggle
to manage the multitude of instructions required to complete the complex tasks. In the single-agent
trajectories, we observe more hallucination in tool parameters and incorrect tool choice.


11


Table 7: Routing Mode Performance



Turn-level
routing Classification
overhead (ms) latency (ms)



Classification
Dataset accuracy



False
switch
rate



Mortgage Routing (First Layer) 0.92 0.00 630 344
Mortgage Routing (Second Layer) 0.92 0.00 630 378
Travel Routing 0.90 0.03 750 360


Table 8: End-to-end evaluation of Routing Mode


Avg. Routing Overhead
Domain Overall GSR Supervisor GSR per Turn (ms)


Travel 0.85 1.00 751
Mortgage 0.95 1.00 627


We report the latency metrics for our experiments in Table 6. When using Claude 3.5 Sonnet
(20241022) for both supervisor agent and specialist agents, the average communication overhead per
turn ranges from 13.39s to 35.44s, with the Software domain showing significantly higher overhead
due to its complexity. The Software domain consistently demonstrates higher latency metrics across
all settings, with user-perceived turn latency reaching 168.73s compared to 31.46s for Travel and
24.42s for Mortgage domains. While the single-agent setting shows lower user-perceived latencies,
this comes at the cost of reduced goal success rates as shown in the previous results. See Appendix C
for full results on coordination mode.


We also performed ablation experiments with the payload referencing capability of the supervisor
agent, which is discussed in more detail in Section 6.1.


**5.2** **Routing Mode Experiments**


To benchmark dynamic agent routing, we curated two additional datasets for evaluation from our
original benchmarking data: 1) Mortgage Routing (3 agent layers) and 2) Travel Routing (2 agent
layers), and manually annotated around 100 routing classification labels for each datasets. Intrinsic
evaluation shows that the LLM-based routing solution with Claude 3.0 Haiku achieves more than
90% routing classification accuracy and less than 3% false agent switching rate (Table 7). Average
latency of routing classification is about 350 ms. With end-to-end evaluation, we observe turn-level
routing overhead (time taken by the supervisor agents) in 600 ms to 800ms range (Table 8).


**5.3** **Agreement with Human Evaluation**


Throughout this report, we have used an LLM to provide automatic judgements on assertions. This
has helped scale our experiments so that we can quickly prototype and develop improved multi-agent
systems. What if we ask a human to judge conversation success purely from their own perspective
without any reference to assertions? To understand how well assertion-based evaluation compares
with human evaluation, we deliver a batch of ninety trajectories to human annotators during one of our
milestone checkpoints. For each conversation, we ask three annotators to provide binary judgements
on a different set of guidelines. During this human evaluation, they are never shown assertions or
LLM judgements and only instructed to determine success and efficiency from their own judgements.
Table 9 show the instructions given to human annotators for each success metric.


After the human annotators finish their evaluation, the aggregated majority judgement is used to
compare against LLM evaluations. Note that for this milestone, we use Claude 3.5 Sonnet (20240620)
for supervisor agent and Sonnet 3.0 for specialist agents. See Appendix D for the automatic and
human evaluation results for this set of experiments. We then compute agreement between human and
LLM judges. Since the judgements for automatic and human evaluation are binary, we use agreement
ratio to measure alignment between human and automatic evaluation. The agreement ratio is the
number of conversations with matching judgements (either both 1 or both 0) over the total number of
conversations evaluated.


12


Table 9: The instructions given to annotators when performing human evaluation of conversation
trajectories. Note that humans do not judge assertions and only determine success purely from their
own judgements.


Metric Human annotator instructions


User GSR Evaluate from user’s perspective, whether the conversation with the primary
agent meets the user’s goals and successfully address user’s requests or not.
System GSR From the perspective of the environment, evaluate whether the actual impacts
of all agent actions accurately address and resolve all of the user’s stated tasks,
requests, and expectations within that specific environment or context.
Supervisor Evaluate from user’s perspective whether the primary agent has tried its best to
GSR help the User, regardless of whether task was completed or the agent actions
correctly impacted the environment.


Table 10: The agreement ratios between human annotators and assertion-based benchmarking on
success metrics across 90 conversation trajectories.


Dataset Overall GSR Supervisor GSR User-side GSR System-side GSR


Travel 0.93 0.87 0.93 0.93
Mortgage 0.87 1.00 0.97 0.87
Software 0.97 0.77 1.00 0.90


For success metrics, the agreement is generally above 85% (Table 10). The only exception is on
primary agent success for software, where the agreement is 77%. Here, the automatic evaluation
has overall GSR as 90% but the human annotators only believe the supervisor agent is successful in
87% of the conversations. On the trajectories where the humans disagree with LLM judgements, we
observe a mix of mistakes from both ends. For some trajectories, the human evaluation would mark
that supervisor agent has not make a mistake but LLM judge has captured when the supervisor agent
repeatedly wanting to follow-up with the user rather than delegating tasks to sub-agents. There is
also the reversed case where the LLM judge does not observe any issues with the supervisor agent
but the human annotators detect that the supervisor agent neglects to conduct thorough code review
with the Review agent.


**6** **Communication Mechanism Ablations**


Section 5 shows the main results of our approach with different models. In this section, we provide
additional ablations to quantify the impact of MAC communication mechanisms. This includes
experiments with and without payload referencing, as well as comparison with open-source frameworks. The additional experiments provide more justification on the utility of MAC for enterprise
applications.


**6.1** **Impact of Payload Referencing**

