<!-- Source: 12-CollabSurvey-2501.06322.pdf | Chunk 4/7 -->


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

The rise of LLM-based multi-agent collaborative systems has been driven by the introduction of
LLMs and their effectiveness as central processing brains. Inspired by human collaboration, these
systems typically break complex tasks into subtasks, with agents assigned specific roles (e.g., software engineer) to focus on subtasks relevant to their expertise. Collaboration channels are critical in
enabling agents to work together, facilitating capabilities such as planning and coordination. These
channels are characterized by their actors (agents involved), type (e.g., cooperation, competition, or
coopetition), structure (e.g., peer-to-peer, centralized, or distributed), and strategy (e.g., role-based,
rule-based, or model-based). Collaboration channels enable communication and task orchestration
while occasionally exhibiting advanced behaviors like the theory of mind [2, 75]. While most works
focus on leveraging LLMs as is - after they are trained, multi-agent collaboration can also be utilized
at other stages as well, such as data sharing, model sharing (federated learning), and fine-tuning
(ensemble learning). However, LLMs are inherently standalone algorithms and are not specifically
trained for collaborative tasks, leaving many mechanisms for leveraging multi-agent collaboration unclear. This presents challenges in both theoretical research and real-world applications,
where agent behaviors can be difficult to explain or predict for stakeholders. Effective coordination


Multi-Agent Collaboration Mechanisms: A Survey of LLMs 21


ensures that the right agent handles the right problem at the right time. However, AI safety and
performance concerns arise, particularly in competitive scenarios where failures like exploitation
and hallucination can happen [22, 34, 153]. Cost, scalability, and efficiency are also critical factors
to consider. Emerging open-source frameworks such as AutoGen [134], CAMEL [74], and crewAI [3]

offer promising tools for building and evaluating multi-agent solutions. Current benchmarks for
LLM-based multi-agent collaborative systems focus on metrics such as success rate, task outcomes,
cost-effectiveness, and collaborative efficiency, providing valuable insights for system improvement.
Through our review and analysis, several key takeaways have emerged that highlight the
strengths, challenges, and opportunities in designing and implementing LLM-based multi-agent
collaborative systems. These lessons provide valuable guidance for researchers and practitioners in
this growing field:


  - **Effective Collaboration Channels** : establishing robust collaboration channels among
agents is crucial for seamless collaboration. Clear protocols prevent misunderstandings
and ensure efficient information exchange. As shown in AutoGen framework [134] MASs
can outperform single-agent systems with effectively designed collaboration mechanisms.
On the other hand, as studied in [128] MAS approach with suboptimal design for their
competitive collaboration channels can be overtaken by single-agent counterpart with
strong prompts.

  - **Collective Domain Knowledge** : incorporating domain-specific knowledge is essential
for designing collaboration architectures and crafting effective system prompts. Often,
collaboration channels are predefined in these cases to align with domain requirements [23,
60, 131].

  - **Adaptive Role and Collaboration Channel Assignment** : in certain tasks, it is better to let the system dynamically assigning roles and collaboration channels based on
agents’ strengths and task requirements enhance system flexibility and performance [39].
This adaptability allows the system to respond effectively to changing environments and
objectives.

  - **Optimal Collaborative Strategy** : for tasks requiring rigorous adherence to established
procedures, rule-based protocols ensure consistency and fairness - avoiding biases caused
by role importance or inherent probabilistic nature in other protocols. Role-based strategies
allow agents to leverage their own expertise effectively in (pre-)structured tasks requiring
job specialization, while model-based protocols work well with uncertain or dynamic
situations that demand adaptability and contextually informed decision-making.

  - **Scalability Considerations** : as the number of agents increases, maintaining coordination
becomes more complex. Implementing scalable architectures and algorithms is essential to
handle larger agent networks without performance degradation.

  - **Ethical and Safety Considerations** : ensuring that agents operate within ethical boundaries and do not engage in harmful behaviors is vital. Implementing safety protocols and
ethical guidelines helps prevent unintended consequences.


**5** **Applications**

This section explores real-world implementations of LLM-based MASs across three dominant
domains, including 5G/B6G and Industry 5.0 (IOT); Natural Language Generation (NLG); and Social
and Cultural Domains (S&C). Table 6 provides a summary of represented works, highlighting their
contributions, advantages, and disadvantages.


[3https://github.com/crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)


22 Tran et al.


Table 6. Summary of applications of different MASs across domains


**Methods** **Domain** **Key Contributions** **Advantages** **Disadvantages** **Refs.**


f


i



LLM-SC IOT - Leverage LLM as the
knowledge generator to enhance the semantic decoder.

LaMoSC IOT - Proposes an LLM-driven
multimodal fusion semantic
communication.

LAM-MSC IOT - Design joint encoder for
multi-modal data.

             - LLM operates as a knowledge generator.

GMAC IOT - Utilize LLM to achieve semantic alignment between
observed states and natural
language, and compress semantic information.

LLM-Blender NLG - Ensemble approaches of
various LLM agents for candidate ranking.

SOT NLG - Generate the skeleton of
answer.

             - Complete the contents of
each skeleton in parallel. f


i




- Achieves significant coding gains. - High computation resources due to the [130]
utilization of LLM.


f


i




- Robust in significantly low SNR condi- - High computation resources due to
tions. the utilization of LLM and Vision Transformer.


f


i




[157]


f


i




- One encoder and decoder can handle various types of data.

- Achieves better coding rates and reconstruction error.

- Improves convergence rate.

- Enable multi-agent collaboration without
communications.


f


i




- High computation resources due to the [65]
utilization of LLM.


- High computation resources due to the [160]
utilization of LLM.


f


i




- Ability to generate outputs better than - To achieve optimal solution, need O( _𝑛_ ~~[2]~~ )
the existing candidates. inference times, leads to computation
overheads.


f


i




- Accelerate inference speed with parallel.

- Suitable for questions that require long
answers (need planned structure).

f


i




- Answer quality evaluation is far from
perfect due to limited prompt set.

- May hurt serving throughput due to parallel requests from diferent agents.f


i



f

Meta- NLG - Construct high-level meta - Maintain coherent line of reasoning. - Elevated cost with multiple model calls.
Prompting prompt to instruct LLMs. - Tapping into a varierty of expert roles. - Requirement for substantial scale and
considerable context window.


i



f


MAD NLG - Two agents express their
own arguments.

              - A judge monitors and manages the debate.

FORD NLG - Include three-stage debate:
1) fair debate, 2) mismatched
debate, 3) roundtable debate.


ChatDev NLG - Employs a chat chain
to break each phase into
smaller subtasks, enabling
multi-turn communication
among agents to collaboratively develop solutions.

AgentVerse NLG - Composed of four stages:
expert recruitment, collaborative decision making, action execution, evaluation.

AgentCoord S&C - Structured representation
for coordination strategy.

            - Three-stage method to
transform general goal into
executable strategies.

OpenAI’s NLG - Routines & Handoffs for
Swarm multi-agent orchestration

              - Lightweight framework for
coordination & execution

TE S&C - Simulate a representative
sample of human participants in subject research. i

AgentInstruct S&C - Generates diverse natural
language data with iterative
cross-agent refinement, including cultural data

SocialMind S&C - Integrates verbal, nonverbal, and social cues to
generate in-situ suggestions
via augmented reality
glasses.

CulturePark S&C - Prompts LLM-based agents
with various cultural backgrounds to simulate crosscultural communication.

Mango S&C - Extracts high-quality
knowledge from LLM-based
agents through prompting
on concepts and cultures.



f


- Reduce bias and distorted perception. - Requires high computational cost due

- Encourages unlimited external feedback. to long debate.

                     - LLMs struggle to maintain coherence
and relevance in long scenarios.


i



f


- Allow LLMs to explore differences between their own understandings and the
conceptualization of others via debate.


i



f


- Can not cover various tasks besides commonsense reasoning.

- Intensively based on the multiple choice
task, which limits FORD’s generalization.


i



f


- Minimizes coding halluciations, where - Without clear, detailed requirements,
the provided source code is missing. agents struggle to grasp task ideas.

                     - Automating the evaluation of generalpurpose software is highly complex.

                      - Multiple agents require more token and
times, resulting computational demands.


i



f


- Improves the generalizability of LLMs in
finding uncertain. • Improve the adaptability of agents.


- Streamline the representing and exploring coordination strategies.

- Minimize repetitive instances of agent
engagement.


- Suitable for applications that require scalability

- Handoff mechanism allows for seamless
transitions between specialized agents

- Enables simulation of different human behaviors, and reveals consistent distortions
of the simulation. i

- Ables to train more capable models from
generated data through tools usage, agentic
capabilities, etc.



f


- Challenges in communication among
agents during the collaborative decisionmaking process.


- Only supports coordinating agents to
collaborate in a plain text environment.

- Only supports static coordination strategy design.


- Concern mainly with role-based protocol & centralised/decentralized structure

- Not yet production-ready


- More human behaviors and additional
LLMs needed to study to ensure the key
findings.
