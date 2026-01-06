<!-- Source: 18-Multi-Agent_Architecture_Taxonomy_LLM.pdf | Chunk 3/4 -->

|7|**Bounded Autonomy:**<br>|Task management or-<br><br><br>|Agents self-organize<br>|Collaboration strategy<br>|Agents select from a<br>|
|7|Self-Organizing & Inte-<br>grated (L2 & L0)|ganically<br>based<br>on<br>current needs.|based on current sce-<br>nario.|evolves organically.|evolves organically.|
|8|**User-Guided Auton-**<br>|User-guided<br>self-<br><br>|User-guided<br>agent<br>|User-guided collabora-<br>|User-guided<br>self-<br><br>|
|8|**omy:** Self-Organizing<br>& User-Guided (L2 &<br>L1)|organizing<br>task<br>management.|self-organization.|tion evolution.|tion evolution.|
|9|**User-Responsive**<br><br>|Self-organizing<br>task<br>|Agent<br>self-<br>|Collaboration<br>evolu-<br>|Self-organized selec-<br>|

Organizing & RealTime Responsive (L2
& L2)



management adjusted
during runtime.



organization adjusted
during runtime.



tion adjusted during
runtime.



tion from contextual resources adjusted during runtime.



Table 2: Mapping autonomy and alignment levels ( _vertical_, #1–9 resulting from Table 1) to architectural
viewpoints ( _horizontal_ ) on autonomous LLM-powered multi-agent systems resulting in 36 viewpoint-specific
system configurations. A detailed explanation of the autonomy and alignment levels is provided in Section 4.1.
For an overview of the applied viewpoints, refer to Section 4.2.


In the following Section 4.3.2, we explore further viewpoint-specific aspects and their interdependencies, in
order to derive level criteria for the taxonomic classification.


**4.3.2** **Viewpoint-specific Aspects and Level Criteria**


As outlined above, architectural viewpoints provide means to analyze certain aspects and aspect relations of
the system’s architecture in a multi-perspective manner [64]. Drawing from the domain-ontology model (Fig.
4), we now systematize the viewpoint-specific aspects employed in our taxonomy. Subsequently, we specify
level criteria for autonomy and alignment corresponding to each aspect. Furthermore, we outline the main
interdependencies among these aspects.


Fig. 8 gives an overview of our taxonomy’s characteristics, structured through a feature diagram [5, 69].
Employed predominantly in software engineering, feature diagrams visually express feature models, which
aim to organize the hierarchical structure as well as dependencies among system features.


In particular, Fig. 8 (a) structures the viewpoint-specific taxonomic structure. Each of the four integrated
viewpoints provides a certain combination of autonomy and alignment levels. As illustrated in Figs. 8 (b–e),
this structure is refined by viewpoint-specific aspects and their interdependencies in terms of requirementsdriven dependencies ( _adapts-to_ ), presuming a high-autonomy system configuration, as discussed in Section
4.2.2. These dependencies suggest that the capabilities of a dependent aspect evolve in line with the needs
and stipulations of the aspect it points to. In turn, also these viewpoint-specific aspects can be assessed by the
autonomy and alignment levels, resulting in a more nuanced taxonomic classification.


21


Figure 8: Feature diagram showcasing the taxonomic structure. Each viewpoint integrates autonomy and
alignment levels **(a)** . The diagram further illustrates viewpoint-specific aspects and mechanisms **(b–e)** alongside
the _adapts-to_ dependencies among them.


Across the four distinct viewpoints, a total of 12 characteristic aspects are identified (as illustrated in Fig.
8). Each of these aspects can be assessed and classified by its corresponding autonomy and alignment
levels, yielding 9 possible configuration options per aspect (detailed in Table 1). Thus, given the viewpoints
_V_ 1 _, V_ 2 _, V_ 3 _, V_ 4 with respective aspect counts _A_ 1 = _A_ 2 = 3, _A_ 3 = 4, and _A_ 4 = 2, and a level count _L_ = 3 for
both autonomy and alignment, we define:



_TA_ =



4

- _Ai,_ (Total Aspects) (1)


_i_ =1



_SC_ = _L_ [2] _,_ (Single Configuration Options per Aspect) (2)
_TSC_ = _TASC,_ (Total Single Configuration Options) (3)

_TCC_ = ( _L_ [2] ) _[A]_ [1][+] _[A]_ [2][+] _[A]_ [3][+] _[A]_ [4] = _SC_ _[T][A]_ _[.]_ (Total Combined Configurations) (4)


Using the provided values, we find _TSC_ = 108 and _TCC_ = 9 [12] _≈_ 282 _×_ 10 [9] .


22


In sum, mapping the autonomy-alignment matrix onto the identified aspects, our taxonomy captures 108
distinct single configuration options. When considering all possible combinations of these configurations,
we arrive at a total of 9 [12], which equates to roughly 282 billion combinations available for configuring
LLM-powered multi-agent architectures. This underscores the complexity challenge posed by such systems,
further accentuated by the various options for intertwined dependencies, as detailed in Section 4.2.2.


In the following, we outline these viewpoint-specific aspects, drawing from the architectural specifications
detailed in Section 3.2 and define corresponding criteria for the levels of autonomy and alignment.


G **Aspects and Levels of Goal-driven Task Management.**


Taxonomic aspects of `Goal-driven Task Management` comprise the three constituting phases:
`Decomposition` (how the goal or complex task is broken down into manageable sub-tasks), `Orchestration`
(how these tasks are distributed among the LLM-powered agents), and `Synthesis` (how the results of the
tasks are finally combined); refer to Fig. 8 (b).


**Level Criteria:**


    - **Static Autonomy (L0)** : At this level, we observe scripted processes and automated mechanics with
rule-based options and alternatives for the task-management activity, including the phases of task
decomposition, distributing and orchestrating the execution of single tasks, or combining their results.
These scripted automated processes might demonstrate variability and flexibility including iterations
based on predetermined mechanics and conditions. However, this level also includes strict processes
or execution chains with no variations.

    - **Adaptive Autonomy (L1)** : Here, the system provides predefined but adaptive procedures for the
phases of the task-management activity. Based on these predefinitions integrated into the system’s
design and implementation, the LLM-powered agents are vested with certain autonomy to adapt
the managing and controlling of the task-management processes. For example, within a defined
framework, the agents are involved in managing the task decomposition, the distribution to other
agents, or decisions about the synthesis of results. For this purpose, also patterns or prepared
mechanics are reused.

    - **Self-Organizing Autonomy (L2)** : This level embodies the LLM-powered agents’ capability to
architect and implement their own strategy for deconstructing and solving problems due to the
characteristics or complexity of a given goal. This might also include high-level generic frameworks
scaffolding the agents’ interactions and processes, but leaving space to LLM-powered agents for
effectively self-organizing the phases of the task-management process.

    - **Alignment Levels** : At this juncture, alignment can be seen in terms of information and constraints
regarding the task-management activity, especially regarding the mechanics in the decomposition,
orchestration or synthesis of sub-processes, e.g., decomposition depth or consensus options for the
total result. The alignment is either integrated into the system’s design (L0), configurable by the user
before runtime (L1) or adjustable during runtime (L2).


M **Aspects and Levels of Multi-Agent Collaboration.**


For the taxonomic classification within `Multi-Agent Collaboration`, we consider
`Communication-Protocol Management` (how the collaboration and dialogues between the agents
are managed), `Prompt Engineering` (how prompts are applied during collaboration and executing the
actions), and `Action Management` (how the different kinds of action, such as the delegation or actual
execution of tasks, or the result evaluation, performed by the agents are managed); see Fig. 8 (c)).


**Level Criteria:**


    - **Static Autonomy (L0)** : At this level, collaborative actions and interactions among agents adhere to
a fixed script or set of rules. The communication protocols, prompt use and augmentation, as well
as the management of actions are pre-defined and don’t adjust dynamically based on agent inputs
or environmental changes. Agents communicate, delegate tasks, execute instructions, and evaluate
results based strictly on established, non-adaptable guidelines. Variability in the collaboration process
is minimal and doesn’t account for unforeseen scenarios or complexities.

    - **Adaptive Autonomy (L1)** : This level introduces adaptability of collaboration aspects for LLMpowered agents based on predefined mechanisms. For example, the communication protocol, the
prompt templates, or the management of the agent actions are modifiable. While the foundational


23


mechanisms are preset, the LLM-powered agents can autonomously select and adapt them due to the
evolving requirements of the given scenario. For this purpose, they might reuse prepared mechanisms
or patterns.

    - **Self-Organizing Autonomy (L2)** : Agents operating at this level showcase the capability to independently strategize their collaboration for task execution. Driven by the specific demands of the
set goals and task complexities, these LLM-powered agents actively plan and execute collaboration
strategies that best address the scenario at hand. For instance, LLM-powered agents can self-organize
protocols for collaboration, mechanisms of prompt engineering and negotiate collaboratively the
execution of actions among the agent network.

    - **Alignment Levels:** Relevant considerations include information and constraints linked to collaboration mechanisms and patterns between agents, the specification of prompt templates, constraints for
prompt augmentation, or preferences for the execution of actions. These components can be either
embedded within the system’s design (L0), made available for user configuration before runtime (L1),
or be amenable to real-time adjustments (L2).


A **Aspects and Levels of Agent Composition.**


The aspects of `Agent Composition` applied by the taxonomy comprise `Agent Generation` (how the agents
are created, including the strategies and mechanisms employed), `Role Definition` (how agents’ roles are
specified), `Memory Usage` (how the agents utilize their memory, i.e., how information is summarized and
stored, or how memory is used for reflecting instructions or planning actions), and `Network Management`
(how the constellation and relationships among agents are managed); refer to Fig. 8 (d).


**Level Criteria:**


    - **Static Autonomy (L0)** : This level features a predefined and rule-driven composition and constellation
of agents. Rules and mechanisms manage the creating of agents, select the agent types, and delineate
their roles and competencies. Memory utilization follows predefined mechanisms, as well as the
relationship between agents.

    - **Adaptive Autonomy (L1)** : While a system at this level provides predefined structures, it grants a
degree of flexibility, permitting LLM-powered agents to adapt their composition and constellation
within the given framework and due to given scenarios. For example, agents can replicate instances,
their competencies are extensible and roles and further attributes (such as the size or compression
mode for the agent memory) can be modified. Agents can modify or extend existing relationships,
e.g., by connecting with further agents.

    - **Self-Organizing Autonomy (L2)** : LLM-powered agents operating at this level exhibit the ability
to autonomously define and generate types and establish collaborative networks. The impetus for
such self-organization arises from an acute understanding of the demands and nuances of the given
scenario. Instead of adhering to predefined agent types and roles or relationships, agents dynamically
constitute and organize based on real-time needs.

    - **Alignment Levels:** Pertinent to agent composition are information and constraints regarding their
creation, types, roles, and competencies. Further, the manner in which agents interrelate and how
they are structured within the network holds significance. These mechanics and configurations can
be either deeply embedded into the system’s design (L0), be made configurable by the user before
runtime (L1), or be dynamically adjustable during system operation (L2).


C **Aspects and Levels of Context Interaction.**


For `Context Interaction`, the taxonomic aspects comprise ( `Resources Integration` (how the integration of contextual resources in terms of data, tools, models, and other applications is achieved), and `Resources`
`Utilization` (how these resources are actually utilized for executing tasks); refer to Fig. 8 (e).


**Level Criteria:**


    - **Static Autonomy (L0)** : At this level, contextual resources, including data, expert tools, and specialized foundation models, are rigidly integrated based on the system’s initial design. Their utilization is
organized by predefined rules and patterns relating scenarios and resource application. However, this
level also includes the case that certain or any resources might not be available for use.

    - **Adaptive Autonomy (L1)** : Certain contextual resources are pre-integrated, but the system provides
adaptive mechanisms usable by LLM-powered agents for integrating missing resources when needed.


24


To this end, access to certain APIs might be prepared. Based on predetermined mechanisms, the
LLM-powered agents can flexible determine how to best utilize and combine these provided resources,
tailoring their approach to the unique requirements of the given scenario.

    - **Self-Organizing Autonomy (L2)** : LLM-powered agents possess the autonomy to interface with a
diverse pool of contextual resources (cf. HUGGING FACE). They can discerningly select, integrate,
and harness these resources based on the objectives at hand and the specific challenges they encounter.

    - **Alignment Levels:** Factors to consider encompass information and constraints pertaining to the
integration and application of contextual resources. These may include specifications or guidelines on
which resources to leverage, when and how to integrate them, any limitations on their utilization, and
more. These specifications or guidelines might be built into the system’s design (L0), made available
for user modification prior to runtime (L1), or even be adapted in real time (L2).


In the following Section 5, we explore the application of our taxonomy to real-world LLM-based multi-agent
systems.


**5** **Classification of Selected Systems**


In order to demonstrate the practical utility of our taxonomy, we analyze and classify selected existing
autonomous LLM-powered multi-agent systems. We have chosen a set of seven state-of-the-art multiagent systems for this assessment: AUTOGPT [77], BABYAGI [51], SUPERAGI [79], HUGGINGGPT [70],
METAGPT [28], CAMEL [41], and AGENTGPT [71]. Each of these systems is maintained and available
as open-source project. For basic information on these and further LLM-powered multi-agent systems, refer
to Section 2.2. For each selected system, we gathered relevant information by examining the technical
documentation and research papers, where available, as well as reviewing the code base. We further engaged
with each system to explore its real-time functionalities, with emphasis on alignment mechanisms available
before and during runtime.


In the following sections, we first report on the results of analyzing and classifying the selected systems
(Section 5.1). Then, we compare and interpret the results in Section 5.2.







|LLM-powered<br>Multi-Agent<br>Systems|Goal-driven Task Mgmt.|Col3|Col4|Col5|Col6|Col7|Multi-Agent Collaboration|Col9|Col10|Col11|Col12|Col13|Agent Composition|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Context Interact.|Col23|Col24|Col25|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**LLM-powered**<br>**Multi-Agent**<br>**Systems**|**Decom**|**Decom**|**Orch**|**Orch**|**Synth**|**Synth**|**CommP**|**CommP**|**PrEng**|**PrEng**|**ActM**|**ActM**|**AGen**|**AGen**|**RoleD**|**RoleD**|**MemU**|**MemU**|**NetM**|**NetM**|**Integ**|**Integ**|**Util**|**Util**|
|**LLM-powered**<br>**Multi-Agent**<br>**Systems**|**AU**|**AL**|**AU**|**AL**|**AU**|**AL**|**AU**|**AL**|**AU**|**AL**|**AU**|**AL**|**AU**|**AL**|**AU**|**AL**|**AU**|**AL**|**AU**|**AL**|**AU**|**AL**|**AU**|**AL**|
|**Auto-GPT** [77]|2|0|0|0|1|0|0|0|1|0|2|0|0|0|1|0|0|0|0|0|0|0|2|0|
|**BabyAGI** [51]|2|0|0|0|1|0|0|0|1|0|2|0|0|0|1|0|0|0|0|0|0|0|2|0|
|**SuperAGI** [79]|2|0|1|0|1|1|0|0|1|0|2|0|1|1|2|1|0|1|0|0|0|1|2|1|
|**HuggingGPT** [70]|2|0|1|0|2|0|0|0|2|0|2|0|2|0|2|0|1|0|0|0|2|0|2|0|
|**MetaGPT** [28]|2|0|0|0|2|0|1|0|1|0|2|0|0|0|0|0|0|0|1|0|0|0|2|0|
|**CAMEL** [41]|2|0|0|0|1|0|0|0|1|0|1|0|0|1|1|1|0|0|0|1|0|0|0|0|
|**AgentGPT** [71]|2|1|1|0|1|0|0|0|1|0|2|0|1|1|2|0|0|0|0|0|0|0|2|1|
|**Zapier*** [62]|1|1|0|1|0|1|0|0|0|1|0|1|0|0|0|0|0|0|0|0|0|1|0|1|


Table 3: Assessment of autonomy ( `AU` ) and alignment ( `AL` ) levels across viewpoint-specific aspects of selected
LLM-powered multi-agent systems. Detailed level criteria for viewpoint-specific aspects are discussed in
Section 4.3.2. * ZAPIER, a workflow-automation tool, has been included to contrast the results.


**5.1** **Taxonomic Classification**


The taxonomic classification relies on a detailed assessment of autonomy and alignment levels for viewpointspecific aspects of the systems. Table 3 reports on the results of assessing these levels of autonomy ( `AU` ) and
alignment ( `AL` ) for aspects characterizing the four architectural viewpoints applied by our taxonomy. In particular, for `Goal-driven Task Management`, the aspects of decomposition ( `Decom` ), orchestration ( `Orch` ), and


25


synthesis ( `Synth` ); for `Multi-Agent Collaboration`, the aspects of communication-protocol management
( `CommP` ), prompt engineering ( `PrEng` ), and action management ( `ActM` ); for `Agent Composition`, the aspects
of agent generation ( `AGen` ), role definition ( `RoleD` ), memory usage ( `MemU` ), and network management ( `NetM` );
for `Context Interaction`, the aspects of resource integration ( `Integ` ), and resource utilization `Util` are
distinguished. An overview of these viewpoint-specific aspects and corresponding level criteria applied for
this assessment is provided in Section 4.3.2.


- In order to contrast the classification results, we included ZAPIER [62] into our comparison, a renowned tool
offering the automation of workflows based on user-specified tasks.







**(a)**

Integ


NetM


MemU


**(d)**

Integ


NetM


MemU


**(g)**

Integ


NetM


MemU





SuperAGI


Decom


AGen











**(b)**


Integ


NetM


MemU


**(e)**


Integ


NetM


MemU


**(h)**


Integ


NetM


MemU





**(c)**


Integ


NetM


MemU





**(f)** CAMEL


Decom







Synth


CommP


PrEng


Synth


CommP


PrEng











Integ


NetM


MemU





AGen



BabyAGI


Decom


AGen


MetaGPT


Decom


AGen


Zapier*


Decom


AGen





Synth


CommP


PrEng


Synth


CommP


PrEng


Synth


CommP


PrEng



Synth


CommP


PrEng


Synth


CommP


PrEng


Synth


CommP


PrEng



Auto-GPT


Decom


AGen


HuggingGPT


Decom


AGen


AgentGPT


Decom


AGen









Figure 9: Radar charts illustrating the system profiles based on an assessment of architectural aspects in terms
of autonomy ( _blue graph_ ) and alignment ( _green dashed graph_ ) levels. Detailed assessment data can be found
in Table 3.


Fig. 9 displays the derived autonomy and alignment levels per multi-agent system using radar (or spider) charts

[80]. In particular, architectural aspects form the multiple axes. The level scheme ( `L0`, `L1`, `L2` ) for autonomy
and alignment is depicted by grey circles linking these axes. The blue graph then represents the assessed
autonomy levels, the green dashed graph the corresponding alignment levels.


In what follows, we outline key results from the taxonomic assessment for each system.


26


- **AUTO-GPT** [77] - enables users to specify multiple goals, which are autonomously decomposed
into tasks and then prioritized (L2 autonomy for `Decomposition` ); also see Fig. 9 (a). The system
encompasses three distinct task-management agents: an execution agent, a task-creation agent, and a
task-prioritization agent. All tasks are actually performed by this singular execution agent sequentially
determined by prioritization (L0 autonomy for `Orchestration` ). Following the completion of each
task, the agent evaluates the intermediate results, engaging in self-criticism. The tasks are optionally
re-prioritized. The final result represents an aggregate of all partial results, complemented with a
succinct summary (L1 autonomy `Synthesis` ). The communication between the three agents follows
a predefined communication protocol. `Prompt Engineering` is adaptive based on templates (L1
autonomy). The management of the performed actions is self-organized (L2 autonomy). Agents
in the system are pre-configured and instantiated once, showing L0 autonomy. The `Role` of the
execution agent is adaptive (L1 autonomy). Both `Memory Usage` and `Network Management` adhere
to predefined rules, marking L0 autonomy. AUTO-GPT is equipped with a suite of predefined
contextual resources (L0 autonomy), which are utilized in a self-organizing manner due to the needs
of the scenario, demonstrating L2 autonomy. Across the aspects, the system provides a low level of
user interaction. Beyond the transmission of goals, further user interaction is only available in terms
of authorizing the subsequent execution step, which however, can also be skipped via the _continuous_
_mode_, leaving users with no further intervention capabilities.


- **BABYAGI** [51] - provides very similar functionalities and architectural characteristics to those
demonstrated by AUTO-GPT. This similarity can be visually observed in the radar charts illustrated
in Figs. 9 (a) and (b). In particular, both systems maintain a high-autonomy level regarding goal
`Decomposition`, the management of single actions performed by the task-execution agent, and the
`Utilization` of integrated contextual resources due to the requirements of the given tasks. Furthermore, both systems provide transparency by reporting on the execution agent’s plans and thinking
operations as basis for executing the tasks. They both maintain iterative, but fixed communication
protocols allowing for the task-management agents to organize the decomposition and aspects of
result synthesis. BABYAGI extends the set of task-management agents by a context agent, which
is responsible for context-interaction tasks. In addition, it also allows the user to configure a few
constraints governing the use of the LLM.


- **SUPERAGI** [79] - also allows users to specify a goals or complex task, which are decomposed
autonomously into tasks tackled sequentially by an LLM-powered agents. Thereby, its functionalities
and architectural characteristics are in some regards similar to AUTO-GPT and BABYAGI (see
above). For instance, the executing agent is performing the assigned tasks autonomously, showcasing
L2 autonomy in `Action Management` ; also see Fig. 9 (c). The systems leverages predefined, but
adaptable prompt templates (L1 autonomy for `Prompt Engineering` ). Contextual resources are
also utilized in an autonomous manner, indicative of L2 autonomy. Diverging from its counterparts,
SUPERAGI necessitates that users create a dedicated agent for every distinct goal. In contrast to the
other two systems, the roles of these agents are highly task-adaptive (L2 autonomy) and can be influenced by user, attributing to L1 alignment. Moreover, the `Orchestration` of tasks is more adaptive
(L1 autonomy). A distinctive feature of SUPERAGI is its ability to incorporate various alignment
strategies. For instance, it permits constraints regarding `Memory Usage`, allowing users to cap the
context window’s length, a trait of L1 alignment. In terms of `Context Interaction`, SUPERAGI
comes with an array of pre-configured tools, all of which can be authorized for `Utilization` .
Furthermore, data can be uploaded, empowering agents to seamlessly incorporate and utilize it (L1
alignment). Though SUPERAGI can handle multiple goals and agents, these agents work in parallel,
separately. There is no actual collaboration between the agents, and no further configuration options
for the user, resulting in L0 autonomy and alignment for `Communication Protocol` and `Network`
`Management` .


- **HUGGINGGPT** [70] - follows a different strategy by leveraging the LLM as an autonomous controller
that combines various multi-modal AI models to solve complex tasks. In this, it integrates with the
HUGGING FACE platform that provides a large pool of foundation models available for utilization.
This singular central LLM-powered agent, tailored to solve the given goal, is autonomous in breaking
down the goal or complex task into manageable tasks (L2 autonomy for `Decomposition` ) as well as
in selecting, combining, and applying the appropriate models via prompting, achieving L2 autonomy
for `Integration` and `Utilization` of contextual resources as well as for `Prompt Engineering`,
`Action Management`, `Agent Generation`, `Role Definition` . However, not every aspect of
HUGGINGGPT exhibits such high autonomy. Some procedural aspects are predefined, but adaptive
to the given task, such the high-level process framework consisting of the predefined phases of


27


planning, model selection, task execution, and response generation. Despite its autonomy in many
aspects, HUGGINGGPT does not grant users any further degree of user customization, resulting in L0
alignment for all aspects; see Fig. 9 (d). In sum, based on our autonomy-alignment matrix (see Table
1), the system shows tendency towards `Bounded Autonomy` (#7; L2 autonomy and L0 alignment).


- **METAGPT** [28] - aims to solve complex programming tasks (specifically in Python) by leveraging
the synergies of multiple collaborating LLM-powered role agents. Thereby, the framework simulates
human workflows and responsibilities inherent to software-development project. For this purpose,
the task-management activity comprises distinct phases similar to the waterfall process (such as RE,
design, coding, testing), each with dedicated role agents responsible for autonomously executing
the associated tasks. Each phase delivers certain artefacts then processed by the next phase (e.g.,
design specification). In particular, the user-specified requirements are autonomously transferred
into these different artefacts (L2 autonomy for `Decomposition` ), which are finally also combined
to product a tested software program, achieving L2 autonomy for `Synthesis` ; also see Fig. 9 (e).
As mentioned aove, the actual `Orchestration` follows a defined scheme, termed as _standardized_
_operation process_, resulting in L0 autonomy. Both `Agent Generation` and `Roles` are predefined
(L0 autonomy). Within their designated phases, the agents display pronounced autonomy, exhibiting
adaptability in their `Action Management` corresponding to the specificity of tasks, thereby reaching
L2 autonomy. `Prompt Engineering` is predefined, but adapted for inter-agent collaboration (L1
autonomy). Contextual resources are autonomously utilized as needed, marking L2 autonomy for
`Context Interaction` . Similar to HUGGINGGPT, METAGPT showcases low levels of alignment
for the user (L0), since it provides no further configuration or adjustment options for the user.


- **CAMEL** [41] - aims to explore the potentials of autonomous cooperation among communicative LLM-powered agents to accomplish complex tasks. Similar the most other multi-agent systems, it aspires to handle given user-prompted goals autonomously. To this end, a dedicated
generic task-specifier agent breaks down the goal into a list of manageable tasks (L2 autonomy for
`Decomposition` ), also see Fig. 9 (f). Subsequently, these tasks are processed by a pair of agents working in tandem through a cyclical dialogue pattern, wherein the AI-user agent lays out the directives,
and the AI-assistant agent assumes the role of the executor. This strict modus operandi corresponds to
L0 autonomy in `Orchestration`, `Communication Protocol`, and `Network Management` . The
specific `Roles` of these predefined agent archetypes can be selected by the user (L1 alignment). Augmenting this duo are other specialized agents designed for specific roles, including task allocation and
strategic planning. In contrast to most other analyzed systems (except METAGPT), CAMEL provides
actual collaboration between role agents executing the given tasks. During the task-execution phases,
agents operate with a marked sense of autonomy, achieving L2 in both `Prompt Engineering` and
`Action Management` . Alignment options for the user are provided via the definition of agents,
encompassing their `Roles` and interrelation in the `Network`, resulting in L1 alignment.


- **AGENTGPT** [71] - also strives to accomplish a user-prompted goal by leveraging a single taskexecution agent, who can be created by the user by specifying its goal, resulting in L1 alignment
for `Agent Generation` . The agent systematically addresses tasks, prioritizing them based on a
predefined list and capitalizing on contextual resources, all in a self-organized manner corresponding
to L2 autonomy. In terms of autonomy levels across different facets, it closely mirrors SUPERAGI, as
can be observed in Fig. 9 (c) and (g). However, when it comes to alignment possibilities, AGENTGPT
diverges slightly. On the one hand, it provides no adjustment options regarding the agent’s role or the
`Synthesis` of results (both L0 alignment). On the other hand, it introduces the option to extend the
task list by inserting custom tasks, achieving L1 alignment for `Decomposition` .


- **ZAPIER** [62] - Unlike the other entities discussed, ZAPIER focuses on workflow automation based on
user-specified tasks and does not represent an LLM-powered multi-agent system. Its inclusion in this
classification serves to contrast the results, providing a clearer understanding of the capabilities and
potential limits of LLM-powered systems when juxtaposed with traditional task-oriented automation
platforms. In particular, in ZAPIER, users need to define step-by-step instructions to facilitate the
automation process. The resulting workflows can work in parallel, but lack the capability for direct
inter-task interactions. ZAPIER offers configuration options (pre-runtime) for diverse aspects related to
`Task Management` and `Context Interaction`, resulting L1 alignment; also see Fig. 9 (h). Given
its non-reliance on LLM-powered agents, it naturally secures an L0 ranking in both autonomy and
alignment for agent-centric attributes. Nevertheless, it leverages LLMs to process textual tasks such
as writing emails, or for decomposing user-specified goals into tasks, a feature users can optionally
activate (thus L1 autonomy for `Decomposition` ). Drawing from our autonomy-alignment matrix,
detailed in Table 1, ZAPIER is aptly categorized as `User-Guided Automation` (#2; signifying L0


28


autonomy and L1 alignment). Given its unique positioning as a workflow automation system, ZAPIER
provides an illustrative deviation from these trends. Its strategic approach is distinct, predominantly
showcasing lower levels of autonomy, as the LLMs are only leveraged for specific, limited tasks.
Conversely, it favors a strategy of extensive user-guided alignment, applicable to all except the
agent-specific aspects. Note, however, that alignment here is not applied as an enhancement or
refinement to actually align the system’s operation to the user’s goal or intention, but in terms of
specifications of process steps with detailed instructions essential for the system’s operation.


**5.2** **Comparative Analysis**


In the following, we discuss the distribution of assessed levels (Section 5.2.1) and explore strategies across
system categories (Section 5.2.2).


**5.2.1** **Comparison of Assessed Levels**


Fig. 10 offers an overview of how the assessed levels of autonomy and alignment distribute over the 12
categories of architectural aspects of the seven selected multi-agent systems. Detailed assessment data is
provided in Table 3.


**(a)  Autonomy Levels**

|Col1|Decom|Orch|Synth|CommP|PrEng|ActM|AGen|RoleD|MemU|NetM|Integ|Ul|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|L2|7|0|2|0|1|6|1|3|0|0|1|6|
|L1|0|3|5|1|6|1|2|3|1|1|0|0|
|L0|0|4|0|6|0|0|4|1|6|6|6|1|



**(b)  Alignment Levels**

|Col1|Decom|Orch|Synth|CommP|PrEng|ActM|AGen|RoleD|MemU|NetM|Integ|Ul|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|L2|0|0|0|0|0|0|0|0|0|0|0|0|
|L1|1|0|1|0|0|0|3|2|1|1|1|2|
|L0|6|7|6|7|7|7|4|5|6|6|6|5|



Figure 10: Distribution of identified autonomy and alignment levels across architectural aspects of selected
LLM-powered multi-agent systems, represented as stacked bar charts with corresponding data provided below.


On the one hand, three groups of aspect categories emerge when assessing autonomy levels, each displaying a
certain degree of homogeneity. A detailed representation can be found in Fig. 10 (a).


    - **High-Autonomy Aspects:** Among the systems, we encounter a high-autonomy strategy for certain
aspects, demonstrated by self-organizing and autonomously deciding LLM-powered agents. This
strategy is particularly evident for the decomposition of goals into manageable tasks ( `Decom` ), for the
management of actions, encompassing the actual performance of different task-related actions ( `ActM` ),
as well as for utilizing the contextual resources such as tools and data ( `Util` ). Nearly all systems
delegate the responsibilities for these aspects to the LLM-powered agents, which corresponds to `L2`
autonomy.


29


    - **Medium-Autonomy Aspects:** For other aspects, systems lean towards a semi-autonomous strategy
( `L1` ), featuring predefined mechanisms adaptable by the LLM-powered agents. This is prominently
observed in two aspects. First, in result synthesis ( `Synth` ), by combining the task results guided by a
predefined framework adaptable by the LLM-powered agents. Second, in the engineering of prompts
( `PrEng` ), such during prompt augmentation by adapting predefined prompt templates.


    - **Low-Autonomy Aspects:** Several architectural aspects showcase a deterministic strategy with
rule-based mechanisms and automation, demonstrating `L0` autonomy, which can observed for the
following aspects:


**–** orchestrating and distributing the tasks ( `Orch` ).

**–** guiding the collaboration between the agents ( `CommP` ).

**–** managing the utilization of memory, such as for reflecting and planning ( `MemU` ).

**–** managing the agent network, such as regarding the relationships between the agents ( `NetM` ).

**–** integrating contextual resources ( `Integ` ).


**Variable-Autonomy Aspects:** The autonomy levels for the aspects of agent generation ( `AGen` ) and role
definition ( `RoleD` ) display notable variability, as depicted in Fig. 10 (a). This heterogeneity is reflective of the
different strategies employed by the multi-agent systems under analysis (detailed in Section 5.2.2).


**Integrated and User-Guided Alignment:** Drawing insights from Fig. 10 (b), it emerges that the predominant
strategy across most systems is to maintain lower levels of alignment across all assessed aspects. This primarily
manifests in alignment techniques already integrated into the system architecture (L0 alignment), offering
little to no options for user adjustment. Furthermore, low-autonomy aspects with predefined and automated
mechanisms can be used to control and align other higher-autonomy levels. Thus, these mechanisms can be
seen as manifestations of integrated alignment. However, we observe a noticeable inclination for systems to
provide user-guided alignment (L1) for specific aspect categories, namely the agent generation ( `AGen` ), agent
role definition ( `RoleD` ), and contextual resource utilization ( `Util` ). Furthermore, the data reveals a consistent
lack of real-time responsive alignment options across all examined systems. Nonetheless, in this context, it is
worth mentioning that some systems at least facilitate monitoring functionalities available for system users
(often termed as _verbose mode_ ), which provide transparency of the reasoning and decision-making performed
by the execution agents during task reflection and planning. This transparency grants users the leverage to
either greenlight or halt the impending actions. However, there are no possibilities to further influence the task
planning or execution, such as by adjusting or refining task planning.


**Intertwined Dependencies:** As evident from the radar charts in Fig. 9, a diverse range of autonomy levels
manifests both within and across architectural viewpoints of the analyzed systems. This variance results in
a complex web of _intertwined dependencies_ between the aspects: Certain aspects have to deal with diverse
dependencies. While dependent on predefined mechanisms or resources provided by low-autonomy aspects
( _availability-driven dependencies_ ), they have to adapt dynamically in response to situational imperatives set by
other high-autonomy aspects ( _requirements-driven dependencies_ ). This complexity resulting from intertwined
dependencies can be seen as challenging for ensuring accurate process execution. A detailed description of
these challenges associated with architectural dependencies is provided in Section 4.2.2.


**5.2.2** **Strategies Across System Groups**


We now explore how different categories of systems balance the interplay between autonomy and alignment.
Based on our taxonomic classification and the resulting system profiles as illustrated in Fig. 9, we can categorize
the selected 7 systems under analysis into three distinct system groups, which encompass general-purpose
systems, central-controller systems, and role-agent systems. It’s important to note that our categorization
into these three groups, based on the systems chosen for this exploration, doesn’t capture the entire spectrum
of autonomous LLM-powered multi-agent systems. For a comprehensive overview of existing systems and
system categories, we recommend referring to the recent surveys provided by [84, 95]. In the following, the
key characteristics as observed from the corresponding system profiles are discussed.


    - **General-Purpose Systems**     - representing multi-agent systems designed for and adaptable to a
broad spectrum of tasks and applications. Within the analyzed set of multi-agent systems, the
following fall into this group: AUTO-GPT [77], BABYAGI [51], SUPERAGI [79], and AGENTGPT

[71]. Goals are decomposed autonomously and represented as prioritized task lists (L2 `Decom` ).
They employ a multi-cycle process framework performed by dedicated task-management agents
represented by certain generic agent types, including a single task-execution agent (see Section 3.2).


30


Relations and communications between these agents are strictly predefined, and agent conversations
express as a monologue of the task-execution agent, resulting in low autonomy levels (L0) for
communication protocol ( `CommP` ), and network management ( `NetM` ). The task-related actions are
performed autonomously by the task-execution agent (mostly L2 autonomy `ActM` ). while resource
integration is based on provided mechanisms ( `Integ` ), the resources are selected and utilized by the
LLM-powered in a self-organizing manner (L2 autonomy for `Util` ), except for CAMEL; resulting
in similar autonomy profiles for the aforementioned aspects. Besides from these commonalities,
these systems distinguish in certain characteristics. Both AUTO-GPT and BABYAGI employ generic
task-execution agent, and provide no further alignment options at all. Moreover, these systems
employ a generic task-execution agent with predefined agent roles and relations, reulting in L0
autonomy for `AGen` and `NetM` . In contrast, SUPERAGI and AGENTGPT employ execution agents
with self-organizing agent roles (L2 autonomy for `RoleD` ), an adaptable orchestration process (L1 for
`Orch` ), and some alignment options, especially for agent-specific aspects. Moreover, these systems
employ execution agents, whose roles can be customized by the user (L1 alignment for `AGen` ).

    - **Central LLM Controller**     - marks a third group specialized in leveraging and combining contextual
resources for accomplishing the complex goals. HUGGINGGPT [70] serves as an archetype of such
systems, utilizing resources especially in terms of existing ML models integrated via HUGGING FACE.
As already detailed in Section 5.1, HUGGINGGPT is characterized by a single central LLM-powered
control agent with monologue-based reflection and planning. Language in terms of agent prompts
as generic interface to manage the interplay between multiple specialized foundation models. In
comparison to other systems or system groups, we see the highest levels of autonomy granted to
this central agent (mostly L2); also see Fig. 9 (d). Furthermore, we see a finite and artefact-oriented
process adaptable by the LLM-powered agent for orchestrating the different model-related tasks (L1
autonomy). As already stated above, beyond prompting the task, there are no further user-centric
alignment options (L0 alignment).

    - **Role-Agent Systems**     - employ an interplay or simulation between multiple dedicated roles agents.
This collaboration can serve different purposes, such as simulating a discussion or solving tasks that
demand for a multi-perspective collaboration. With defined roles in a certain environment (such as
in a software development project), their application is bound to this application domain or special
purpose. Among the analyzed systems, METAGPT [28] and CAMEL [41] represent such systems. In
contrast to the general-purpose systems, the execution agents play roles with dedicated responsibilities
in a certain application domain. Furthermore, these role agents actually collaborate directly with
each other. In case of the two exemplary systems, this collaboration is realized by communication
protocols employing a dynamic exchange between agents with instructor and executor roles. In
particular, CAMEL employs two such role agents based on predefined agent types, but adjustable by
the user. In ongoing strict dialogue cycles, the AI-user role agents instructs the AI-assistant role agent
to execute the tasks (L0 autonomy for `CommP` ). Similar to SUPERAGI, CAMEL requires the user to
specify the agents’ roles (L1 alignment). METAGPT, in contrast, internally assigns predefined roles
with responsibilities alongside a waterfall development process (L0 alignment); thus, also expressing
a finite and artefact-oriented process (L0 autonomy for `Orch` ), terminating with the produced and
tested software program. However, like in real-world software project, refinement iterations can
follow, optional feedback cycles make it adaptable for the agents (L1 autonomy for `CommP` ).


**Strategy Assessment.** Beyond differences in the applied communication protocols, it is the flexibility of
agent roles (in relation to both autonomy and alignment) and further customization options for agent-specific
aspects that distinguishes the systems’ strategies (see above). However, when examining how the systems
deal with autonomy and alignment across further aspects, most systems and system groups show similar
strategies. The reasoning capabilities of LLM-powered agents are especially leveraged in areas demanding
high autonomy, such as the goal decomposition, the actual execution of task-related actions, and the utilization
of contextual resources. Interestingly, these high-autonomy aspects are mostly combined with low alignment
levels, resulting in _bounded autonomy_ aspects (refer to Table 1). A closer look at aspect interdependencies, as
depicted in Fig. 8, reveals that these internally _unbalanced_ aspects are accompanied by other low-autonomy
aspects equipped with limited flexibility, as follows:


   - Autonomous decomposition directly depends on the user-prompted goal.

   - Autonomous action management depends on strict or predefined communication protocol.

    - Autonomous resource utilization depends on strict or predefined resource integration.


In these cases, the predefined and rule-based mechanisms serve as integrated alignment guiding and controlling
the accurate operation of the dependent autonomous aspects.


31


Based on the findings of the taxonomic classification, in the next Section 6, we discuss challenges for current
systems and reflect on the taxonomy’s limitations and potentials.


**6** **Discussion**

