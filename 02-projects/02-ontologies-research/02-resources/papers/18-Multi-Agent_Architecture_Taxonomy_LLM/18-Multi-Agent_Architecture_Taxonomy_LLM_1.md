<!-- Source: 18-Multi-Agent_Architecture_Taxonomy_LLM.pdf | Chunk 1/4 -->

## BALANCING AUTONOMY AND ALIGNMENT: A MULTI-DIMENSIONAL TAXONOMY FOR AUTONOMOUS LLM-POWERED MULTI-AGENT ARCHITECTURES

**Thorsten Händler**
Ferdinand Porsche Mobile University of Applied Sciences (FERNFH)
Wiener Neustadt, Austria
```
              thorsten.haendler@fernfh.ac.at

```

**ABSTRACT**


Large language models (LLMs) have revolutionized the field of artificial intelligence, endowing it with sophisticated language understanding and generation capabilities. However,
when faced with more complex and interconnected tasks that demand a profound and iterative thought process, LLMs reveal their inherent limitations. Autonomous LLM-powered
multi-agent systems represent a strategic response to these challenges. Such systems strive
for autonomously tackling user-prompted goals by decomposing them into manageable
tasks and orchestrating their execution and result synthesis through a collective of specialized intelligent agents. Equipped with LLM-powered reasoning capabilities, these agents
harness the cognitive synergy of collaborating with their peers, enhanced by leveraging
contextual resources such as tools and datasets. While these architectures hold promising
potential in amplifying AI capabilities, striking the right balance between different levels of
autonomy and alignment remains the crucial challenge for their effective operation. This
paper proposes a comprehensive multi-dimensional taxonomy, engineered to analyze how
autonomous LLM-powered multi-agent systems balance the dynamic interplay between
autonomy and alignment across various aspects inherent to architectural viewpoints such as
goal-driven task management, agent composition, multi-agent collaboration, and context
interaction. It also includes a domain-ontology model specifying fundamental architectural
concepts. Our taxonomy aims to empower researchers, engineers, and AI practitioners to
systematically analyze, compare, and understand the architectural dynamics and balancing
strategies employed by these increasingly prevalent AI systems, thus contributing to ongoing efforts to develop more reliable and efficient solutions. The exploratory taxonomic
classification of selected representative LLM-powered multi-agent systems illustrates its
practical utility and reveals potential for future research and development.


_**Keywords**_ Taxonomy, autonomous agents, multi-agent collaboration, large language models (LLMs), AI
system classification, alignment, software architecture, architectural viewpoints, software-design rationale,
context interaction, artificial intelligence, domain-ontology diagram, feature diagram, radar chart.


**1** **Introduction**


In recent years, the emergence and the technological feasibility of large language models (LLMs) have
revolutionized the field of artificial intelligence [11, 56, 76, 15, 98]. Pre-trained on vast amounts of text data,
these models have catalyzed significant advancements by enabling sophisticated language understanding and
generation capabilities, opening doors to a broad range of applications [9, 13, 32]. Yet, despite their remarkable
capabilities, LLMs also have inherent limitations.


While LLMs excel at generating outputs based on patterns identified in their training data, they lack a genuine
understanding of the real world. Consequently, their outputs might seem plausible on the surface, but can be


factually incorrect or even _hallucinated_ [45, 30]. Moreover, despite their proficiency in handling vast amounts
of textual information and their rapid processing and pattern recognition capabilities, LLMs struggle with
maintaining consistent logic across extended chains of reasoning. This deficiency hinders their ability to
engage in a deliberate, in-depth, and iterative thought process (aka _slow thinking_ ) [74, 33, 20, 43]. As a result,
LLMs encounter difficulties when it comes to handling more complex and interconnected tasks [37, 90].


These limitations of individual LLMs have led to the exploration of more sophisticated and flexible AI
architectures including multi-agent systems that aim at accomplishing complex tasks, goals, or problems with
the _cognitive synergy_ of multiple autonomous LLM-powered agents [77, 51, 79, 59, 70, 41, 71, 28]. Such
systems tackle user-prompted goals by employing a _divide & conquer_ strategy, by breaking them down into
smaller manageable tasks. These tasks are then assigned to specialized agents, each equipped with a dedicated
role and the reasoning capabilities of an LLM, as well as further competencies by utilizing contextual resources
like data sets, tools, or further foundation models. Taking a cue from Minsky’s _society of mind_ theory [48],
the key to the systems’ problem-solving capability lies in orchestrating the iterative collaboration and mutual
feedback between these more or less _’mindless’_ agents during task execution and result synthesis.


For this purpose, LLM-powered multi-agent systems realize an interaction layer [4]. Externally, this layer
facilitates the interaction between the LLM and its contextual environment. This includes interfacing with
external data sources, tools, models, and other software systems or applications. These external entities can
either generate or modify multi-modal artefacts or initiate further external processes. Internally, the interaction
layer allows for organizing the task-management activity by providing a workspace for the collaboration
between the LLM-powered agents. Thereby, LLM-powered multi-agent systems are characterized by diverse
architectures implementing various architectural design options.


One of the central challenges for the effective operation of LLM-powered multi-agent architectures (as with
many AI systems) lies in finding the optimal _balance between autonomy and alignment_ [97, 10, 66, 92, 28].
On the one hand, the systems should be aligned to the goals and intentions of human users; on the other
hand, the systems should accomplish the user-prompted goal in a self-organizing manner. However, a system
with high autonomy may handle complex tasks efficiently, but risks straying from its intended purpose if not
sufficiently aligned, resulting in unexpected consequences and uncontrollable side effects. Conversely, a highly
aligned system may adhere closely to its intended purpose but may lack the flexibility and initiative to respond
adequately to novel situations. Current systems exhibit diverse approaches and mechanisms to intertwine these
_cross-cutting concerns_ [35] throughout their architectural infrastructure and dynamics.


However, existing taxonomies and analysis frameworks for autonomous systems [12, 94, 44, 21, 78] and
multi-agent systems [7, 19, 82, 50] fall short in providing means to categorize and understand these challenges
and involved architectural complexities posed by LLM-powered multi-agent systems.


This paper aims to bridge this gap by introducing a systematic approach in terms of a comprehensive multidimensional taxonomy. This taxonomy is engineered to analyze and classify how autonomous LLM-powered
multi-agent systems balance the interplay between autonomy and alignment across different architectural
viewpoints, encompassing their inherent aspects and mechanisms.


**Alignment**



_real-time_
_responsive_


_user-_
_guided_


_integrated_



L2


L1


L0



**Autonomy**





**Architectural**
**Viewpoints**


_context interaction_
_multi-agent collaboration_
_agent composition_

_goal-driven task management_



_static / adaptive / self-organizing_


Figure 1: A simplified representation of the proposed multi-dimensional taxonomy for autonomous LLMpowered multi-agent systems. The x-axis represents the level of autonomy, the y-axis the level of alignment,
and the z-axis the four applied architectural viewpoints. Characteristics of LLM-powered multi-agent systems
can be assessed and classified by locating them within this taxonomic structure. For an in-depth discussion of
the taxonomy, refer to Section 4.


2


The proposed taxonomy is built on the identification and specification of architectural characteristics of such
systems. It aims at understanding the complexities arising from the interplay of interdependent architectural
aspects and mechanisms, each characterized by distinct levels of autonomy and alignment. A simplified
overview of the dimensions and levels applied in our taxonomy is represented by the cuboid shown in Fig. 1.


First, the synergy between autonomy and alignment manifests as a two-dimensional matrix with multiple hierarchical levels. This matrix captures a spectrum of nine distinct system configurations, ranging from systems
that strictly adhere to predefined mechanisms ( _rule-driven automation_, L0/L0) to those that dynamically adapt
in real-time, guided by evolving conditions and user feedback ( _user-responsive autonomy_, L2/L2).


Second, these configuration options are not imposed to the LLM-powered multi-agent system flatly. Instead,
they are applied to multiple distinct architectural viewpoints [38], such as the system’s functionality ( _goal-_
_driven task management_ ), its internal structure ( _agent composition_ ), its dynamic interactions ( _multi-agent_
_collaboration_ ) as well as the involvement of contextual resources such as tools and data ( _context interaction_ ).
Stemming from these four viewpoints, we have discerned 12 architectural aspects, each with distinct autonomy
and alignment levels. When integrated into our taxonomic system, they culminate in 108 single configuration
options available for further combination. This granularity facilitates a nuanced analysis and assessment of
the system’s architectural dynamics resulting from the interplay between autonomy and alignment across the
system architecture, laying the foundations for further analysis and reasoning about design decisions.


The contributions of this paper can be categorized as follows:


(1) **Architecture Specification:** We outline the architectural characteristics of autonomous LLMpowered multi-agent systems and propose a domain-ontology model represented as a UML class
diagram structuring the architectural concepts and their interrelations relevant for our taxonomy.

(2) **Multi-dimensional Taxonomy:** We introduce a comprehensive multi-dimensional taxonomy tailored
to analyze and understand how autonomous LLM-powered multi-agent architectures balance the
dynamic interplay between autonomy and alignment across different architectural viewpoints. For
this purpose, our taxonomy provides hierarchical levels for both autonomy and alignment, which
are applied to system viewpoints such as goal-driven task management, agent composition, multiagent collaboration, and context interaction, thus incorporating a third dimension. Level criteria for
autonomy and alignment are specified for several architectural aspects inherent to these viewpoints.

(3) **Taxonomic Classification of Selected Systems:** We demonstrate the applicability and effectiveness
of our taxonomy by assessing and comparing a selection of seven representative autonomous LLMpowered multi-agent systems. This taxonomic classification provides insights into the architectural
dynamics and balancing strategies of the analyzed systems. Moreover, it identifies challenges and
development potentials, not only concerning the interplay between autonomy and alignment. The
application of the taxonomy also serves as a first empirical validation.


Through these contributions, we aim to provide a systematic framework for analyzing, comparing, and
understanding the architectural dynamics and complexities of LLM-powered multi-agent systems, thus
contributing to the ongoing efforts towards building more reliable and efficient multi-agent systems.


**Structure of the Paper.** The remainder of this paper is structured as follows. Section 2 discusses related work
on taxonomies for intelligent systems and gives an overview of existing autonomous LLM-based multi-agent
systems. Section 3 outlines the key characteristics and specifies foundational concepts of autonomous LLMpowered multi-agent architectures relevant for the taxonomy. In Section 4, we introduce our multi-dimensional
taxonomy, which incorporates specifications of autonomy and alignment levels and their application to
architectural viewpoints and aspects of LLM-powered multi-agent systems. Section 5 showcases the utility of
our taxonomy, as we analyze and categorize selected current multi-agent systems. In Section 6, we discuss the
insights gained from this analysis. Finally, Section 7 concludes the paper.


**2** **Background and Related Work**


In this section, we discuss the application of taxonomies for autonomous agents and multi-agent systems
(Section 2.1) and give an overview of the state-of-the-art of LLM-powered multi-agent systems (Section 2.2).


**2.1** **Taxonomies and Intelligent Systems**


Taxonomies represent structured classification schemes employed to categorize objects in a hierarchical manner
according to specific criteria. They are a popular means for structuring, measuring or comparing various


3


kinds of approaches such as methods, techniques or technologies. They find applications in a wide range of
disciplines and domains such as software engineering [81] or explainable artificial intelligence (XAI) [2].


The field of intelligent and autonomous systems spans a variety of configurations and operational structures,
with some systems operating as individual entities and others involving multiple interacting agents. Reflecting
this variety, the taxonomies proposed over the years have largely followed two main trajectories: those focusing
on autonomous systems and those focusing on multi-agent systems.


**Taxonomies for Autonomous Systems** mainly categorize systems based on the level and type of autonomy,
intelligence, learning capabilities, and ability to interact with their environment. These taxonomies, such as
those by [94, 12, 44, 21, 78], are essential for understanding the spectrum of capabilities and complexities
inherent to these systems. In particular, Wooldridge and Jennings [94] present a comprehensive taxonomy
that classifies intelligent agents based on key properties such as autonomy, social ability, reactivity, and
proactiveness. Their classification sheds light on the independent operational capabilities of single-agent
systems. In addition, Brustoloni [12] introduces a taxonomy centered around the idea of autonomy levels,
drawing the distinction between autonomous, semi-autonomous, and non-autonomous systems. This provides
a valuable lens through which the extent of an agent’s independence can be analyzed. Maes’ taxonomy [44]
focuses on situating agents within a landscape defined by their reasoning and learning capabilities. The work
provides a robust framework for assessing the cognitive dimensions of an agent, ranging from reflex agents to
learning agents. Franklin and Graesser [21], in their work, delve into the interaction between autonomous
agents and their environment, leading to a taxonomy that is heavily contextual and environmental-dependent.
Lastly, Tosic and Agha [78] put forth a taxonomy that embraces the diversity in the field, offering a multifaceted perspective on autonomous agents, taking into consideration their design, behavior, and interaction
capabilities. Besides these scientific frameworks, further industry-focused and more pragmatic taxonomies
are in use, such as the taxonomy provided by SAE international [29] serving as a foundational standard
for self-driving cars with definitions for levels of driving automation; from no driving automation to full
automation.


However, while these taxonomies offer valuable insights into the capabilities and behaviors of autonomous
systems, they don’t inherently address the complexity and nuances involved when multiple agents powered by
large language models are working together within a multi-agent architecture. Hence, the need for a dedicated
taxonomy for such systems is evident.


**Taxonomies for Multi-Agent Systems**, on the other hand, extend beyond the confines of individual agent
characteristics, integrating the dynamics of interactions and collaborations among multiple agents. The
landscape of multi-agent systems taxonomies provides various works focusing on different aspects of these
complex systems [7, 19, 82, 50]. In particular, Bird et al. developed a taxonomy rooted in the communication
and cooperation strategies among agents, investigating crucial factors such as communication methods, task
decomposition, resource sharing, and conflict resolution [7]. Similarly, Dudek et al. offered a taxonomy
specifically for multi-robot systems [19]. This taxonomy, while primarily focusing on robotic applications,
can be generalized to other multi-agent systems, considering important aspects like team size, communication
topology, team organization, and team composition. In a different vein, Van Dyke Parunak et al. proposed a
taxonomy for distributed AI systems, putting emphasis on environmental aspects and interaction modalities,
thus highlighting the importance of the agents’ ability to interact with and manipulate their environment [82].
Further broadening the field, Moya et al. proposed a comprehensive taxonomy for multi-agent systems based
on characteristics such as the nature of the agents, the environment in which they operate, the communication
protocols they use, and the tasks they perform [50]. The taxonomy also thoroughly examined the various types
of interactions among the agents, including cooperation, coordination, and negotiation.


While these taxonomies have contributed significantly to our understanding of communication protocols and
agent constellation within multi-agent systems, they were developed prior to the advent of large language
models (LLMs), and thus do not encapsulate the characteristic challenges associated with LLM-based multiagent architectures. In this context, autonomous agents, also as members of multi-agent networks, often
have been used as a kind of metaphor [21] for intelligent and interacting components following rule-based
communication protocols and bundling a set of specific skills to interact with their environment (e.g., equipped
with certain sensors and actuators, cf. multi-robot systems [19]). LLMs have introduced a new degree of
reasoning capabilities, enabling the creation of genuinely intelligent agents operating within collaborative
networks in an autonomous manner.


Moreover, while the concepts of autonomy and alignment are often discussed in AI literature [52, 65] and
also the system’s architecture plays a fundamental role in software engineering [4], none of the existing
taxonomies for autonomous systems or for multi-agent systems has so far applied a systematic approach to


4


either investigate architectural aspects or combine the concepts of autonomy and alignment for analyzing the
systems.


In the light of these limitations, our work seeks to develop a new taxonomy specifically tailored to LLMpowered multi-agent systems. Our aim is to provide a taxonomy that captures the unique aspects and challenges
of LLM-powered architectures, especially with regard to how autonomy and alignment are balanced across
architectural aspects and viewpoints, offering a systematic framework for understanding and designing these
complex systems.


**2.2** **Current LLM-based Agent Systems**


The advent and widespread use of large language models (LLMs) like GPT-3 [11] have opened up new
opportunities for creating increasingly sophisticated and human-like AI systems. These models empower
the design of intelligent agents with advanced capabilities to comprehend and generate human-like text, thus
enriching the interaction and experience for end-users. However, the application of LLMs also brings forth
several challenges, as highlighted by [32]. Among these, one main challenge lies in handling task complexity,
particularly when dealing with intricate tasks that necessitate a well-coordinated execution of numerous
interconnected sub-tasks [70] and the interaction with further tools and data. In response to this, autonomous
multi-agent systems utilizing the reasoning abilities of LLMs have emerged. These systems address complexity
by intelligently breaking down larger goals into manageable tasks, which are then accomplished by multiple
collaborating agents specializing in a specific role and equipped with distinct competencies. For this purpose,
these systems realize an _interaction layer_ [4] providing a workspace for multiple collaborating agents,
each connected with an LLM. The reasoning competencies are enhanced, as needed, by the agent’s access
to contextual resources, such as specific expert tools, data sets, further foundation models, and external
applications, which allow the agents to gain information from and to impact their environment by creating or
modifying multi-modal artefacts or by triggering external processes. The agents collaborate, bringing their
capabilities to bear on the problem, and their results are subsequently combined to achieve the overall goal.


Currently, several projects are established that aim at realizing such autonomous AI architectures for accomplishing complex tasks based on multiple interacting agents and powered by large language models
(LLMs). Exemplary but representative autonomous multi-agent systems are AUTOGPT [77], BABYAGI

[51], SUPERAGI [79], HUGGINGGPT [70], CAMEL [41], AGENTGPT [71] and METAGPT [28]. For a
categorization and comparison of these selected system architectures using the developed taxonomy, see
Section 5. Among these systems, we can distinguish those providing general-purpose task management and
problem solving with generic agent types and collaboration mechanics [77, 51, 79, 70] and those systems
designed for specific application domains with corresponding domain agents and processes, such as for the
domain of software development [28, 41, 61].


Some of these recent multi-agent systems as well as further related projects such as GORILLA [60] or VOYAGER

[83] are built upon the LANGCHAIN Python framework [14], which allows to realize the aforementioned
interaction layer to define agents and chains of tasks as well as the access to and interplay between large
language models and contextual resources in terms of data resources (such as vector databases [31]) or various
expert tools. For this purpose, predefined components such as agent types and prompt templates, such as for
data interaction, can be reused.


Besides these open-source software projects, further scientific projects and approaches are identifiable that
leverage multiple agents or personas powered by LLMs for task management and problem solving [88, 26].
Moreover, the interplay between multiple LLM-powered agents is also addressed in other related contexts,
such as for simulating the interaction between multiple personas or roles [59, 22], especially with focus on
debating and thereby addressing challenges of hallucinations [18] or the _degeneration-of-thought (DoT)_ [42],
or for developing conversations and behavior provided by non-playable characters (NPCs) in role-playing
video games [17].


A recent survey of LLM-powered autonomous agents is provided by [84], which focuses on investigating
and comparing the agents’ characteristics and capabilities in terms of profile generation, memory operations
and structures, planning, tool integration and learning strategies. Complementing this, another recent survey

[95] offers an expansive overview of existing approaches, contextualizing them with foundational technical,
methodical, and conceptual paradigms formative for LLM-powered multi-agent systems.


However, as we dive into the specifics of current autonomous LLM-powered multi-agent systems, striking
the right balance between autonomy and alignment emerges as a central challenge. These AI systems must
navigate a fine line – being autonomous enough to organize the interplay between multiple LLM-powered


5


agents and contextual resources to accomplish complex tasks consisting of various interconnected sub-tasks,
but also adequately aligned to the intentions and goals of users. This especially proves challenging, since the
specified and prompted user goal might not exactly represent the user’s intentions [8], resulting in unexpected
consequences and uncontrollable side effects.


Given the exploratory state of the field, current systems exhibit a wide range of architectures, each with its
unique blend of autonomy and alignment dispersed across various architectural components and mechanisms.
The diversity in these systems illuminates the different strategies and designs adopted to address this balancing.
However, it also signifies the lack of a systematic approach, underscoring the importance of a taxonomy that
can provide a structured understanding and comparison of these systems.


**3** **Architecture Specification**


In this section, we specify architectural foundations relevant for our taxonomy. Section 3.1 provides an
overview of architectural and behavioral characteristics of autonomous LLM-powered multi-agent systems.
Following this, we delve deeper into the architectural key concepts and their interrelationships through a
domain-ontology model (see Section 3.2).



**Human**
**User**

























**System**
**Architect**


|interacts<br>with|User Interface<br>Prompt<br>Preferences<br>Response|Col3|Agent-Interaction Layer<br>G<br>Task<br>Goal ...<br>break<br>down Task<br>Result<br>synthesis<br>executes<br>A<br>M<br>collaborate<br>Prompt<br>Agent<br>Prompt<br>Agent<br>Role Memory<br>B<br>Alignment Techniques|develops|
|---|---|---|---|---|
|interacts<br>with|**User Interface**<br>Respon~~s~~e<br>Promp~~t~~<br>Preferen~~c~~es||Alignment Techniques<br>Memory<br>Role<br>Prompt<br>Prompt<br>collaborate<br>executes<br>B<br>synthesis<br>**Agent**<br>**Agent**<br>**Agent-Interaction Layer**<br>A<br>break<br>down<br>Goal<br>Task<br>Task<br>Result<br>**...**<br>M<br>G|<br> <br>specifies|



Figure 2: Overview of the primary characteristics of autonomous multi-agent systems powered by large
language models (LLMs) and enhanced by contextual resources like tools and data. A description of these
characteristics is provided in Section 3.1, and for an in-depth exploration of architectural concepts, refer to
Section 3.2.


**3.1** **Characteristics Overview**


In the following, we outline the main architectural characteristics of autonomous LLM-powered multi-agent
systems, as illustrated in Fig. 2.


G **Goal-driven Task Management.** Autonomous LLM-powered multi-agent systems are designed
to accomplish user-prompted goals or complex tasks. For this purpose, the system employs an
interactive and multi-perspective strategy for problem solving, often referred to as deep reasoning or
_slow thinking_ [33] enabled by the capabilities of large language models (LLMs) and the advantages of
contextual resources. When faced with such challenges, the system adeptly breaks down the complex
task into smaller, manageable tasks. These sub-tasks are subsequently distributed among various
agents, each equipped with specific competencies. A crucial aspect of this _divide & conquer_ strategy
lies in the effective orchestration of these interconnected sub-tasks and the subsequent synthesis of
partial results, ensuring a seamless and cohesive final result.


6


A **LLM-Powered Intelligent Agents.** At the core of these systems, intelligent agents structure the
system as the foundational components. Each agent is endowed with a unique set of competencies,
which include a clearly defined role, an individual memory, as well as access to further contextual
resources, such as data, tools, or foundation models (see below), required for solving the tasks
assigned to them. The backbone of their reasoning and interpretative capabilities is rooted in the
incorporation of large language models (LLMs). This enables the agents not only to reflect upon the
tasks or to plan and process the assigned tasks efficiently, but also to access and utilize contextual
resources, as well as to communicate with other agents.


M **Multi-Agent Collaboration.** The interaction layer provides the workspace for a network of such
collaborating LLM-powered agents. While executing the assigned tasks, these specialized agents
collaborate with each other via prompt-driven message exchanges to delegate responsibilities, seek
assistance, or evaluate the results of tasks undertaken by their peers. Key to the agents’ collaboration is
to effectively combine the strengths of each agent to collectively meet the defined goals, exemplifying
_cognitive synergy_ . While individual skills are important, the power of these systems emerges from
the coordinated efforts of the collective, a concept articulated by Minsky in his idea of the _society of_
_mind_ [48].


C **Context Interaction.** Some tasks require the utilization of contextual resources, such as expert
tools, data, further specialized foundation models, or other applications. These resources extend their
ability to gather environmental information, create or modify artefacts, or initiate external processes.
Leveraging these resources enables the agents to better understand and respond to their operational
context and to effectively execute complex tasks. This capacity for contextual adaptation, augmented
by the integration of various resources, contributes to a more versatile and comprehensive system that
can address diverse challenges and requirements.


B **Balancing Autonomy and Alignment.** The dynamics of LLM-powered multi-agent systems are
characterized by a complex interplay between autonomy and alignment. As captured in Fig. 3, this
complexity can be traced back to the triadic interplay and inherent tensions among the primary
_decision-making entities_ : human users, LLM-powered agents, and governing mechanisms or rules
integrated into the system. _Alignment_, in this context, ensures that the system’s actions are in sync
with human intentions and values. On the other side of the spectrum, _autonomy_ denotes the agents’
inherent capacity for self-organized strategy and operation, allowing them to function independent
of predefined _rules and mechanism_ and without human _supervision_ . Moreover, in systems steered
by user-prompted goals, it becomes pivotal to differentiate between generic alignment aspects, in
terms of _mechanisms_ predefined by system architects to inform core functionalities, and user-specific
preferences _customized_ by the system users themselves.


**Human**
**User**


Automation / Autonomy

**System Operation**



**Rules &**
**Mechanisms**



**LLM-powered**
**Agents**



Figure 3: Triadic interplay and dynamic tensions between the decision-making entities in LLM-powered
multi-agent systems.


However, from an architectural perspective, autonomy and alignment transform into _cross-cutting_
_concerns_ [35]. They traverse components and mechanisms across the entirety of the system’s
architecture, influencing the communication between agents, the interaction with contextual resources,
and more. Achieving a balanced configuration of autonomy and alignment is a crucial challenge,
which directly impacts the system’s efficiency and effectiveness.


7


In the following Section 3.2, we elaborate on the architectural details of these characteristics.






|Col1|Create<br>Task|
|---|---|
|||


































|Col1|Task|
|---|---|
|||













































































































































































































Figure 4: Domain-ontology model represented as UML class diagram structuring selected architectural
concepts and concept relations relevant for the domain of autonomous LLM-powered multi-agent systems.
For a comprehensive exploration of this model, refer to Section 3.2.


**3.2** **Specification of Architectural Components**


Fig. 4 illustrates a structured overview of selected concepts and their interrelations relevant for the addressed
domain of autonomous LLM-powered multi-agent systems in terms of a domain-ontology model. Domain
ontologies, embraced across fields from philosophy to information systems, facilitate a shared understanding
of domain-specific concepts [75]. While they aid automated knowledge dissemination among software entities


8


as _formal ontologies_ [23], they are also devised as _conceptual models_ to support human understanding of the
addressed domain [36, 24, 25].


Our domain ontology is represented as a conceptual model in terms of a class diagram of the _Unified Modeling_
_Language (UML2)_ [55], which allows for organizing the identified concepts as classes and their relationships
in terms of generalizations and kinds of associations with indicated multiplicities (i.e. amount of objects
involved in a relationship). For further details on the applied diagram notations, the UML specification serves
as a comprehensive guide [55].


The primary objective of the presented model in Fig. 4 is to mirror architectural concepts especially relevant to
our taxonomy’s scope. In doing so, it deliberately adopts a high-level view, abstracting from technical details
and specifics typical of individual systems to support clarity and accessibility. For example, while diving into
the complexities of the agent’s memory usage, as for reflecting and combining task instructions or for planning
steps and actions, is undoubtedly worthy of thorough exploration [59, 85], it falls outside the narrow scope of
our taxonomy. This approach ensures that actual multi-agent systems can be regarded as potential instances of
this conceptual framework. It’s worth noting that this doesn’t preclude the addition of more specific technical
components and mechanisms as systems evolve.


The domain-ontology model derives from an examination of the code and architectural documentation of
several representative multi-agent architectures, especially AUTOGPT [77], SUPERAGI [79], and METAGPT

[28], the _Generative Agents_ project [59], as well as the LANGCHAIN framework [14]. The latter serves as the
foundational infrastructure for some of the assessed multi-agent systems (refer to Section 2.2). Through an
iterative process, we analyzed these systems and frameworks to understand their components, interactions, and
overarching structures. This analysis facilitated the identification and abstraction of recurrent architectural
characteristics prevalent among these architectures.


The concepts of the model are arranged into thematic blocks corresponding to the system characteristics
identified in Section 3.1, such as G . In the following, we delve into these concepts and their main interrelations.
Further details are provided in the domain-ontology diagram illustrated in Fig. 4.


G **Concepts of Goal-driven Task Management.** Typically, a `Human User` initiates system operations via a
`User Prompt` through the `User Interface` . Most of these systems employ _single-turn prompting_ to convey
intricate `Goals` [68]. The prompts can be enriched with detailed instructions, exemplifications like reasoning
sequences [90], role specifications, or output expectations [32]. Systems may also permit the definition of
`Preferences` to better align AI operations with user objectives. Besides textual user input, speech, images,
videos, or mode combinations are conceivable, for example. Internally, this user-prompted `Goal` (which might
represent a directive, problem, question, or mission) undergoes decomposition into `Tasks` or `Sub-Tasks` to
be manageable by the `Agents` . These tasks can be interconnected in different ways, such as _sequential tasks_
or _graph tasks_ [70], which requires appropriate task prioritization. Task decomposition is the first of three core
phases within the `Task-Management Activity` :


    - `Decomposition` : Breaking down complex tasks into manageable `Tasks` and `Sub-Tasks` ; optionally
resolving dependencies between them, resulting in a prioritized list of `Tasks` .


    - `Orchestration` : Organizing the distribution and delegation of `Tasks` among suitable `Agents` .


    - `Synthesis` : Evaluating and combining `Task Results` as well as finally presenting a unified `Total`
`Result` .


Furthermore, each `Task-Management Activity` embodies an `Activity Log` and an `Activity Memory` .
To maintain transparency and traceability of all `Actions` performed, an `Activity Log` captures all relevant
action details throughout an activity, while the `Activity Memory` distills and retains key insights. In addition,
systems might feature a `Library`, a repository storing best practices, lessons learned, or reusable knowledge,
such as `Prompt Templates` [91] or specific information like API credentials. `Actions` within this activity
are delegated to specialized `Agents` —each characterized by a distinct `Role`, `Type`, and further competencies.
Essential for the actions’ success is their interaction with various kinds `Context` —ranging from `Data`
and expert `Tools` to foundational `Models` (detailed below). Once all partial tasks are completed, the `Task`
`Results` are integrated and combined into a `Total Result` addressing the prompted `Goal` . This result
might also include multiple `Artefacts`, encompassing text, graphics, multimedia, and more. The nature
and involvement of tools applied, such as `Execution` or `Development Tools`, can lead to varied `Impacts`,
such as triggering external processes. Finally, the `Response`, a summation of the result, is relayed to the user
through the user interface.


9


A **Concepts of LLM-Powered Intelligent Agents.** Within each `Task-Management Activity`, a set
of intelligent `Agents` collaborate, forming a multi-agent `Network` . These agents derive their advanced
reasoning capabilities from `Large Language Models` (LLMs) [11, 32, 53], which are involved in performing
different kinds of `Actions`, each related to a certain `Task` and/or contributing to its `Task Result` . Each
agent is differentiated by its unique `Role` in the activity and possesses an individual `Memory` —a repository
that encompasses condensed experiences and knowledge gained by the agent. It can manifest in multiple
formats—be it textual records, structured databases, or embeddings. Oriented to human memorization, in multiagent systems, we also see a combination of short-term memory (i.e., compressed information transmission via
the context window) and approaches for long-term memory [87, 86], such as by leveraging vector databases
(see below). The encapsulated history of the agent’s actions might also be chronicled in an `Actions Log` .
Furthermore, different generic `Agent` types can be distinguished in terms of their roles, and their unique
functionalities within the collaborative agent network.


    - `Task-Management Agents` : These agents are specialized in organizing the processes related to the
task-management activity [77, 51, 41].


**–** `Task-Creation Agent` : Generating new tasks, which optionally also includes deriving tasks
by breaking down complex tasks.

**–** `Task-Prioritization Agent` : Assigning urgency or importance to tasks, which includes to
resolve the dependencies between the tasks.

**–** `Task-Execution Agent` : Ensuring efficient task completion.

    - `Domain Role Agents` : These agents are domain-specific experts. They excel in specialized roles
within the application domain [59], collaborating with peer role agents when needed. Examples
encompass roles in the software-development process, such as project manager, software architect,
developer, or QA engineer [28, 41].

    - `Technical Agents` : These agents are tech-savvies, typically tasked with interfacing with technical
platforms or development tools. Exemplary technical agents are represented by the `SQL Agent` for
database interactions or the `Python Agent` for developing Python scripts [14, 28].


An essential distinction to note is the variability in agent memory reliance. While some agents harness the
power of memory or an action log, e.g., for reflecting or planning tasks, others function devoid of these
recollections. Specifically, for technical aspects or actions that demand an unprejudiced or unbiased lens,
agents without memories are often preferred.


M **Concepts of Multi-Agent Collaboration.** As detailed above, each `Task-Management Activity`
involves a set of multiple collaborating `Agents` with different roles and competencies as well as driven by the
reasoning capabilities of utilized large language models (LLMs). This reasoning power enables the agents to
reflect, plan and process the assigned tasks [85, 59] as well as to interact with other agents [28]. In particular,
the `Agents` execute different kinds of `Actions` which in sum aim at achieving the user-prompted `Goal` . In
particular, the following sub-types of `Action` performed by the `Agents` can be distinguished:


    - `DecomposeTask` : Breaking down a task into multiple sub-tasks, optionally ordering and prioritizing
the tasks.

    - `Create Task` : Defining and generating new tasks.

    - `DelegateTask` : Delegating a task to another agent, addressed as `Receiver` .

    - `ExecuteTask` : Actually executing a given task.

    - `EvaluateResult` : Assessing the outcomes of a task.

    - `MergeResult` : Integrating or combining two or more task results.


Thereby, each `Action` can be part of another `Action`, which are, however, performed in the context of a certain
phase of the `Task-Management Activity` (see Fig. 4). Furthermore, each `Action` can include multiple
interactions with an LLM. The LLM’s reasoning capabilities are employed in multiple directions within an
`Action`, such as for reflecting memories and instructions, observing existing results, planning steps and/or
weighing options to proceed [85, 59, 28]. For this purpose, an `Agent Prompt` generated by an `Agent` and
triggered within a certain `Action` is send to and then processed by the LLM, which generates a `Response`
informing and/or guiding the next steps within the triggering action. An action might also include `Context`
`Utilization` . Before the LLM receives the `Agent Prompt`, it may undergo `Prompt Augmentation` [72].
This process can integrate additional specifics like the aspects or parts of the agent’s `Role` or `Memory`,


10


`Context Information` (e.g., data excerpts) acquired from previous `Context Utilization`, or chosen
`Prompt Templates` prepared and/or adapted for certain kinds of actions [14]. Such agent-driven _prompt_
_engineering_ is pivotal for LLM-powered multi-agent systems.


Direct collaborations involving two or more agents typically rely on prompt-driven communication sequences
or cycles. For instance, a `Delegate Task` action directed at a `receiver` agent might convey information,
place a request, initiate a query, or suggest a potential course of action. Subsequently, the `Evaluate Result`
action provides feedback by validating or refuting, and agreeing or disagreeing with the presented results [93].
A `Communication Protocol` provides a structured framework and methodology for agents’ collaboration,
guiding the execution of specific `Actions` by establishing rules and mechanisms for message exchanges
within the multi-agent network [73, 39, 93]. For instance, in LLM-powered multi-agent systems, the following
distinct protocols are observable, each built upon the basic mechanisms of an interplay between instruction
and execution, with optional subsequent result evaluation:


    - _Strict finite processes_ or execution chains with predefined action sequences, interactions between
predefined agents, and typically having a well-defined endpoint, which might represent the production
of a specific output or artefact [28].


    - _Dialogue cycles_ characterized by alternating `DelegateTask` and `ExecuteTask` actions between two
agents, creating a feedback loop of instruction and execution [41].


    - _Multi-cycle process frameworks_ with interactions between generic agent types, allowing for greater
dynamism in agent interactions [77, 51].


In all these exemplary cases, dedicated `Agent Types` are defined and coupled with the corresponding types
of `Action` . Further details are discussed in Section 5.2.


C **Concepts of Context Interaction.** For executing the task-related actions, the LLM-powered agents are
able to leverage specialized competencies and further information provided by additional `Context` which can
be distinguished into `Tools`, `Data`, and `Foundation Models` [70] (see Fig. 4).
