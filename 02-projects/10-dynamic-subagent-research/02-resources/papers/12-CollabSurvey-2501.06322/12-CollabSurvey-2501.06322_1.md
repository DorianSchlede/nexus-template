<!-- Source: 12-CollabSurvey-2501.06322.pdf | Chunk 1/7 -->

### **Multi-Agent Collaboration Mechanisms: A Survey of LLMs**

[KHANH-TUNG TRAN, School of Computer Science and Information Technology, University College](HTTPS://ORCID.ORG/0000-0001-6796-8911)

Cork, Ireland
DUNG DAO, School of Computer Science and Information Technology, University College Cork, Ireland
MINH-DUONG NGUYEN, Department of Information Convergence Engineering, Pusan National

University, South Korea
QUOC-VIET PHAM, School of Computer Science and Statistics, Trinity College Dublin, Ireland
BARRY O’SULLIVAN, School of Computer Science and Information Technology, University College Cork,

Ireland
HOANG D. NGUYEN [∗], School of Computer Science and Information Technology, University College

Cork, Ireland


With recent advances in Large Language Models (LLMs), Agentic AI has become phenomenal in real-world
applications, moving toward multiple LLM-based agents to perceive, learn, reason, and act collaboratively.
These LLM-based Multi-Agent Systems (MASs) enable groups of intelligent agents to coordinate and solve
complex tasks collectively at scale, transitioning from isolated models to collaboration-centric approaches. This
work provides an extensive survey of the collaborative aspect of MASs and introduces an extensible framework
to guide future research. Our framework characterizes collaboration mechanisms based on key dimensions:
actors (agents involved), types (e.g., cooperation, competition, or coopetition), structures (e.g., peer-to-peer,
centralized, or distributed), strategies (e.g., role-based or model-based), and coordination protocols. Through a
review of existing methodologies, our findings serve as a foundation for demystifying and advancing LLMbased MASs toward more intelligent and collaborative solutions for complex, real-world use cases. In addition,
various applications of MASs across diverse domains, including 5G/6G networks, Industry 5.0, question
answering, and social and cultural settings, are also investigated, demonstrating their wider adoption and
broader impacts. Finally, we identify key lessons learned, open challenges, and potential research directions of
MASs towards artificial collective intelligence.


CCS Concepts: • **General and reference** → **Surveys and overviews** ; • **Computing methodologies** →
**Multi-agent systems** ; _Natural language generation_ ; _Neural networks_ .


Additional Key Words and Phrases: Artificial Intelligence, Large Language Model, Multi-Agent Collaboration


**Reference:** Khanh-Tung Tran, Dung Dao, Minh-Duong Nguyen, Quoc-Viet Pham, Barry O’Sullivan,
and Hoang D. Nguyen. 2025. Multi-Agent Collaboration Mechanisms: A Survey of LLMs. arXiv
preprint (2025), 35 pages.


∗Corresponding author.


[Authors’ Contact Information: Khanh-Tung Tran, 123128577@umail.ucc.ie, School of Computer Science and Information](https://orcid.org/0000-0001-6796-8911)
Technology, University College Cork, Cork, Ireland; Dung Dao, School of Computer Science and Information Technology,
University College Cork, Cork, Ireland, 123122658@umail.ucc.ie; Minh-Duong Nguyen, Department of Information Convergence Engineering, Pusan National University, Busan, South Korea, duongnm@pusan.ac.kr; Quoc-Viet Pham, School of
Computer Science and Statistics, Trinity College Dublin, Dublin 2, D02PN40, Ireland, viet.pham@tcd.ie; Barry O’Sullivan,
School of Computer Science and Information Technology, University College Cork, Cork, Ireland, b.osullivan@cs.ucc.ie;
Hoang D. Nguyen, School of Computer Science and Information Technology, University College Cork, Cork, Ireland,
hn@cs.ucc.ie.


2 Tran et al.


**1** **Introduction**


**1.1** **Motivation**

Recent advancements in Large Language Models (LLMs) have transformed artificial intelligence
(AI), enabling them to perform sophisticated tasks such as creative writing, reasoning, and decisionmaking, arguably comparable to human level [156]. While these models have shown remarkable
capabilities individually, they still suffer from intrinsic limitations such as hallucination [57], autoregressive nature (e.g., incapable of slow-thinking [49]), and scaling laws [55, 69]. To address these
challenges, agentic AI leverages LLMs as the brain, or the orchestrator, integrating them with
external tools and agenda such as planning, enabling LLM-based agents to take actions, solve
complex problems, and learn and interact with external environments [1,2] . Furthermore, researchers
are increasingly exploring horizontal scaling — leveraging multiple LLM-based agents to work
together collaboratively towards collective intelligence. This approach aligns with ongoing research
in Multi-Agent Systems (MASs) and collaborative AI, which focus on enabling groups of intelligent
agents to coordinate, share knowledge, and solve problems collectively. The convergence of these
fields has given rise to LLM-based MASs, which harness the collective intelligence of multiple LLMs
to tackle complex, multi-step challenges [118]. Inspiration for MASs extends beyond technological
advancements and finds roots in human collective intelligence (e.g., society of mind [87], theory of
mind [45]). Human societies excel in leveraging teamwork and specialization to achieve shared
goals, from everyday tasks to scientific discoveries. Similarly, MASs are designed to emulate these
principles, enabling AI agents to collaborate effectively by combining their individual strengths
and perspectives.
LLM-based MAS can have multiple collaboration channels with different characteristics, as
illustrated in Fig. 1. MASs have demonstrated notable successes across various domains, enhancing
the capabilities of individual LLMs by leveraging collaboration and coordination among specialized
agents. These systems distribute tasks among agents, allowing agents to share knowledge, execute
subtasks, and align their efforts toward shared objectives. The potential benefits of MASs are
transformative. They excel in knowledge memorization, enabling distributed agents to retain
and share diverse knowledge bases without overloading a single system [51, 154]. They enhance
long-term planning by delegating tasks across agents, supporting persistent problem-solving
over extended interactions [58]. Furthermore, MASs enable effective generalization by pooling
expertise from multiple models with specialized prompts/personas, allowing them to address diverse
problems more effectively than standalone models. Lastly, MASs improve interaction efficiency
by simultaneously managing subtasks through specialized agents, accelerating the resolution of
complex, multi-step tasks. MAS strives to achieve collective intelligence, where the combined
capabilities of multiple agents exceed the sum of their individual contributions [24].
One of the main focus for effective MASs is the mechanisms of collaboration [33, 74, 75, 97, 132],
which lead to a transition from traditional, isolated models toward approaches that emphasize
interactions, enabling agents to connect, negotiate, make decisions, plan, and act jointly, driving
forward the capabilities of AI in collective settings. A deeper understanding of how collaboration
mechanisms operate in MASs is critical to unlocking their full potential.


[1https://blogs.nvidia.com/blog/what-is-agentic-ai/](https://blogs.nvidia.com/blog/what-is-agentic-ai/)
[2https://www.ibm.com/think/insights/agentic-ai](https://www.ibm.com/think/insights/agentic-ai)


Multi-Agent Collaboration Mechanisms: A Survey of LLMs 3





















Fig. 1. Example question-answering application of LLM-based multi-agent collaborative system. In the first
collaboration channel, two LLMs are collaborating through a debate against each other, given the input
by the user with a turn-based strategy. In the second channel, the Oppose Agent cooperates and leverages
information from Research Agents, and provides the final response to the user.


**1.2** **State-of-the-Arts and Contributions**

Due to the importance and timely need for LLM-based multi-agent collaborative systems, there
have been a couple of surveys on this topic. However, these works often fall short in fully addressing
the collaborative aspects and mechanisms of LLM-based MASs, which are crucial to enabling agents
to work effectively toward shared goals, as summarized in Table 1. For instance, [47, 107, 136]
focus on single-agent systems and only touch on multi-agent collaboration at a surface level.

[136] lays the groundwork by proposing a framework for LLM-based agents, consisting of three
components: brain, perception, and action. Their work highlights the use of LLMs as the brain
of agents, leveraging techniques such as input modality integration, prompting, retrieval, and
tool usage. However, their discussion of multi-agent collaboration is limited to agent behaviors
and personalities, lacking an exploration of mechanisms that enable agents to work together. [47]
surveys the domains and settings where LLM-based MASs have been successfully applied, profiling
the communication structures of these systems (layered, decentralized, centralized, and shared
message pools) but without touching other characteristics of collaboration, such as type, strategy,
or coordination architecture.
Other works, such as [82], focus on collaborative strategies, categorizing them into merging,
ensemble, and cooperation. Although their survey discusses how these strategies are applied to
LLMs and extends cooperation beyond traditional fusion techniques, it overlooks other essential
collaboration mechanisms, such as competition and coopetition, and dimensions beyond popular
collaboration types. In contrast, [120] proposes a generic framework for enhancing LLM capabilities
via MASs, showing how tools like Auto-GPT align with their framework. However, the collaboration
mechanisms remain conceptual, lacking detailed implementation and characterization. In [50], the
focus is on configuring LLMs to leverage diverse capabilities and roles, such as integrating memory
and information retrieval components. Their exploration of multi-agent collaboration primarily
centers on planning and orchestration architectures, emphasizing global and local task planning
based on agent roles and specializations. Meanwhile, [46] narrows its focus to the application of


4 Tran et al.


Table 1. Summary of related surveys on LLM-based multi-agent collaborative system.



**Focus on Multi-**
**Refs.** **Agent Collaborative**
**System**



**Review of Collaborative**
**Aspects and Mechanisms**
**in MAS**



**Propose General**
**Framework for**
**MAS**



**Review of Real-**
**World Applications**




[136] Low Low None None

[70] Low Low None Low

[82] Medium Low None None

[50] Medium Low None Low

[68] Medium Low None Low

[120] Medium None Low Medium

[46] Medium Low None Medium

[47] Medium Low Medium High
OURS High High High High


LLM-based MASs in agent-based modeling and simulation, discussing challenges such as environment perception, human alignment, action generation, and evaluation. While insightful for
simulation-specific applications, it lacks a broader perspective on in-depth collaborative mechanisms. Similarly, [68] surveys these systems for digital twin applications, while [52, 70] focuses on
the domain of software engineering.
From the summary and explanation above, there are clear gaps in fully exploring the collaborative
aspects and mechanisms of LLM-based MASs, which are crucial for enabling agents to work
together toward shared goals. This work aims to provide a comprehensive view of the collaborative
foundations between LLM-based agents in multi-agent collaborative systems. With collaboration
as the main focus, our study characterizes collaborations between agents based on their actors
(agents involved), type (e.g., cooperation, competition, or coopetition), structure (e.g., peer-to-peer,
centralized, or distributed), and strategy (e.g., role-based, rule-based, or model-based), and the
coordination layer in collaborations. We emphasize the mechanisms and know-how that facilitate
effective collaboration, identifying key characteristics and trends in MAS design. Through a survey
of existing approaches and identification of open challenges, we synthesize these findings into a
cohesive framework. This framework serves as a foundation for future research, advancing the
integration of LLMs in MASs and paving the way for more adaptable, intelligent, and cooperative
AI systems capable of addressing complex, real-world applications.
Our main contributions are listed as follows:


  - **Collaborative Aspects and Mechanisms in LLM-based MAS** : we focus on the operational mechanisms of LLM-based multi-agent collaboration, emphasizing the "know-how"
required to enable effective collaboration, including the collaboration type, strategy, communication structure and coordination architecture.

  - **General Framework for LLM-based MAS** : we present a comprehensive framework,
integrating diverse characteristics of MAS, allowing researchers to understand, design and
develop multi-agent collaborative systems.

  - **Review of Real-World Applications** : we examine real-world implementations of LLMbased MASs across various domains, highlighting their practical applications, successes,
and limitations.

  - **Discussion of Lessons Learned and Open Problems** : we identify key challenges in the
developmental agenda of MASs, such as collective reasoning and decision-making, and
outline potential research directions to address these challenges.


Multi-Agent Collaboration Mechanisms: A Survey of LLMs 5


**1.3** **Paper Organization**


This paper is organized as follows. Section 2 provides the background necessary for understanding
this work, including an overview of LLMs, MASs, and collaborative AI. In Section 3, we introduce
foundational concepts in LLM-based multi-agent collaborative systems through mathematical
notations, emphasizing the vital role of collaboration. Then, in Section 4, we present an extensive
review of LLM-based multi-agent collaborative systems, categorized by key characteristics of
collaboration, including type, strategy, structure, and coordination and orchestration. Next, Section 5
reviews key applications of LLM-based multi-agent collaborative systems across both industry and
academia. In Section 6, we discuss open problems and potential future research directions in this
relatively new and evolving research area. Finally, we conclude this survey paper on LLM-based
multi-agent collaborative system in Section 7.


**2** **Background**


**2.1** **Multi-Agent (AI) Systems**

MAS is a computerized system composed of multiple interacting intelligent agents. The key
components of MAS are as follows:


   - Agents: The core actors with roles, capabilities, behaviors and knowledge models. Capabilities like learning, planning, reasoning and decision making lend intelligence to the agents
and overall system.

   - Environment: The external world where agents are situated in and can sense and act upon.
Environments can be simulated or physical spaces like factories, roads, power grids etc.

   - Interactions: Communications between agents happen via standard agent communication
languages. Agent interactions involve cooperation, coordination, negotiation and more
based on system needs.

   - Organization: Agents either have hierarchical control or organize based on emergent behaviors.


MASs can solve problems that are difficult or impossible for an individual agent or a monolithic
system to solve [37]. Agents collaboratively solve tasks yet they offer more flexibility due to
their inherent ability to learn and make autonomous decisions. Agents use their interactions with
neighboring agents or with the environment to learn new contexts and actions. Subsequently,
agents use their knowledge to decide and perform an action on the environment to solve their
assigned tasks [43]. It is this flexibility that makes MAS suited to solve problems in a variety of
disciplines including computer science, civil engineering, and electrical engineering.
The salient features of MAS, including flexibility, and reliability, self-organization, and real-time
operation make it an effective solution to solve complex tasks, which can be detailed as follows:


   - Flexibility and Scalability: MAS can flexibly adapt to changing environments by adding,
removing, and modifying agents. This makes them highly scalable for solving complex
problems.

   - Robustness and Reliability: Decentralization of control leads to continued system operation
even with some failed components. This lends greater robustness and fault tolerance.

   - Self-Organization and Coordination: Agents can self-organize based on emergent behavior
rules for the division of labor, coordinated decision making, and conflict resolution.

   - Real-time Operation: Immediate situational responses are possible without the need for
human oversight. Enables applications like disaster rescue and traffic optimization.


Their efficiency stems from the division of labor inherent in MAS whereby a complex task is divided
into multiple smaller tasks, each of which is assigned to a distinct agent. Naturally, the associated


6 Tran et al.


overheads, e.g., processing and energy consumption, are amortized across the multiple agents,
which often results in a low-cost solution as compared to an approach where the entire complex
problem is to be solved by one single powerful entity. Each agent can solve the allocated tasks with
any level of pre-defined knowledge which introduces high flexibility. The distributed nature of
problem solving adopted in MAS also imparts high reliability. In the event of agent failure, the task
can be readily reassigned to other agents.


**2.2** **Large Language Models**

LLMs - driven by the development of transformer architectures [127] - represent a significant
leap in Natural Language Processing (NLP) and AI. These models, such as OpenAI’s GPT [4],
Meta’s LLaMA [124], and Google’s Gemini series [123], are trained on vast text corpora and
rely on large-scale artificial neural networks with billions, sometimes trillions, of parameters.
Their scale has enabled breakthroughs in language understanding, generation, and task-specific
applications [38, 93, 101, 110, 125].
The defining characteristic of LLMs is their size and the phenomenon of emergent abilities, which
arise when models exceed a certain threshold in terms of parameters. These emergent behaviors
allow LLMs to solve tasks they were not explicitly trained on, such as analogical reasoning and
zero-shot learning, where the model can tackle new problems without additional fine-tuning [113].
The launch of models like GPT-3 and ChatGPT in recent years has made these capabilities accessible
to the public, leading to a surge in both academic and industrial research on how to optimize, scale,
and secure LLMs for real-world use [42].
Despite the promising innovations, LLMs are not without challenges. Their performance degrades as real-world knowledge changes, prompting a focus on aligning models with up-to-date
information without retraining from scratch [19, 28]. Moreover, the geopolitical and ethical implications of LLM development have become the limelight for policymakers, especially concerning
the computational power required and potential misuse by malicious actors [76, 86].
LLMs are increasingly being utilized as the "brain" for individual agents in MASs, bringing
sophisticated reasoning and language capabilities to each agent. With frameworks like AgentVerse, LLMs enhance agents’ autonomy by allowing them to infer tasks, make decisions based
on situational awareness, and even exhibit emergent social behaviors such as collaboration and
negotiation [24]. While LLMs have shown remarkable performance in single-agent tasks, their
limitations become apparent in multi-agent settings where the complexity of coordination, communication, and decision-making is higher. Issues such as cascading hallucinations — where one
erroneous output leads to compounding mistakes pose challenges in sustained multi-agent interactions. However, frameworks like MetaGPT introduce meta-programming techniques including
structured workflows and processes within agent interactions to decompose and tackle complex
problems, mitigating these issues [56]. Moreover, consensus-seeking mechanisms like those tested
in the Consensus-LLM project show that LLMs can negotiate and align on shared goals in dynamic
environments [21]. These works showcase LLMs’ potential as central decision-making components
and highlight LLMs’ capacity to adapt to the strategies of other LLM-based agents, which could be
foundational in multiple applications.


**2.3** **Collaborative AI**

Collaborative AI often refers to AI systems designed to work together with other AI agents or
humans [27]. Collaborative AI emerges from two primary research directions: 1) the advancements
of AI which resulted in increasingly effective tools for human use and a growing demand for AI
systems that can collaborate with other agents (humans or AI models), and 2) the realization that
active collaboration among AI models can significantly enhance efficiency and effectiveness. This


Multi-Agent Collaboration Mechanisms: A Survey of LLMs 7


research spans various domains, including MASs, human-machine interaction, game theory, and
natural language processing [1, 14, 26, 29]. By integrating these technologies, collaborative AI has
the potential to drive novel applications with profound economic and societal impacts [85, 96].
Collaboration is the key in enabling AI agents to interact and work with each other. A straightforward collaboration mechanism would be two models cooperate together towards a shared
goal. While cooperation is a fundamental aspect, the collaboration spectrum extends further, encompassing advanced mechanisms like competition and coopetition. Collaborative AI leads to a
transition from traditional, isolated models toward approaches that emphasize collaboration. New
methodologies have been proposed to enable agents to interact, negotiate, make decisions, plan,
and act jointly, driving forward the capabilities of AI in collective settings [30].
A major topic of Collaborative AI is MAS research, which focuses on the interactions between
intelligent agents and emergent collaborative behaviors. More specifically, MASs are interested
in agents, or AI models, that can learn, adapt, and collaborate with one another in complex
environments, towards a common shared goal. On the other hand, the rapid advancement of LLMs
has enabled new possibilities. LLMs have been shown to be capable of serving as the “brains”
behind agents in MASs, driving applications where agents not only perform tasks but interact with
external tools (e.g., internet searches, calculators), and, more significantly, with each other [47].
However, LLMs are not inherently designed and trained to communicate with one another, leaving
a wide array of potential applications and open problems in this area. The fusion of LLMs and
MASs promises exciting opportunities for further exploration and innovation.
This work provides a comprehensive view of the collaborative aspect between LLM-based agents
in MASs, emphasizing the mechanisms that enable agents to work effectively toward shared goals.
By surveying existing approaches and identifying open challenges in this emerging research area,
we offer a unique perspective that extends beyond traditional cooperation to include diverse modes
of collaboration, such as debate, negotiation, and competition. This in-depth focus on collaborative
dynamics positions our work as an essential resource for advancing the integration of LLMs in
MASs, paving the way for more adaptable, intelligent, and collaborative AI systems with enhanced
capabilities for real-world applications.


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













