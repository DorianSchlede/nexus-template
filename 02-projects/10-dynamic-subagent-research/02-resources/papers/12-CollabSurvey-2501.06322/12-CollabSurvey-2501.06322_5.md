<!-- Source: 12-CollabSurvey-2501.06322.pdf | Chunk 5/7 -->


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




[64]


[95]


f

[119]


[77]


[140]


[105]


[24]


[97]


See:
4


[36]


i



f


i

- Requires human to hand-construct gen- [88]
eration flows.



f


i


- Designs and leverages a multi-modal, as - Requires advanced edge hardware to [144]
multi-tier collaborative agent system. handle complex systems.



f


i


- Generated data allow training models - Still depends on LLM’s knowledge of
with less bias and democratization. each culture, and hence limited results
for low-resource cultures.



f


i


[73]



f


i


- Automated method allows for generating - Human evaluations need to be from [94]
a large amount of resources. more diverse backgrounds.


Multi-Agent Collaboration Mechanisms: A Survey of LLMs 23

























Fig. 6. LLM-based MAS-enabled semantic communication system framework, leveraging LLMs directly to
the physical layer coding and decoding of communication system [130].


**5.1** **5G/B6G and Industry 5.0**


Recently, LLM has emerged to be an efficient tool to significantly improve the performance of edge
networks [66, 108, 116].
**5G and B6G Wireless Network.** LLM-SC [130] proposed a novel framework, which utilizes
LLM technology to model the semantic information of text and design a semantic communication
system based on LLMs (see Fig. 6). By using LLM to probabilistically model transmitted language
sequences, LLM-SC achieves a communication paradigm that balances both semantic-level and
technical-level performance. LaMoSC [157] introduces an LLM-driven multimodal fusion semantic
communication system to extend unimodal transmission and improve generalization. By leveraging the extensive external knowledge of LLMs to generate prompt text, LaMoSC overcomes
the limitations of conventional semantic communication systems’ knowledge bases and restricted
generalization capabilities. To enhance multimodal communication, a fusion encoder is designed to
integrate textual and visual features from the LLM using an attention mechanism. LAM-MSC [65]
presents a novel application of LLMs to enhance multimodal semantic communication frameworks.
In particular, the study introduces a multimodal alignment (MMA) mechanism based on a multimodal language model (MLM), utilizing CoDi for modality transformation. This MMA supports
the synchronized generation of integrated modalities by constructing a shared multimodal space.
Furthermore, to enable the comprehension of personal information, the framework incorporates a
knowledge base powered by an LLM, specifically leveraging GPT-4. Authors in [145] propose a
novel framework called M2GSC. In this framework, the LLM serves as shared knowledge base, plays
three critical roles, including complex task decomposition, semantic representation specification,
and semantic translation and mapping. It also spawns a series of benefits such as semantic encoding
standardization and semantic decoding personalization. GMAC [160] introduces a data transmission strategy based on semantic information extraction to reduce the volume of data transmitted
in MASs effectively. In this framework, GMAC employs LLMs to achieve semantic alignment
between observed states and natural language, facilitating compressed semantic communication.
This approach enhances bandwidth efficiency by extracting and compressing relevant information,
thereby optimizing data transmission in multi-agent communication. The authors in [121] propose
MSADM, an end-to-end health management framework for dynamic heterogeneous networks.
Using local and neighboring information, MSADM covers all stages of the health management life
cycle, including anomaly detection, fault diagnosis, and mitigation. By integrating an LLM as a
facilitating agent, MSADM efficiently collects and processes abnormal data, reducing diagnostic
errors caused by inconsistent data representations. The authors in [78] propose a novel approach


24 Tran et al.


that integrates LLMs with reconfigurable intelligent surfaces (RIS) to enable energy-efficient and
reliable communication in the Internet of Vehicles. In this RIS system, the LLM is used to deduce
optimized strategies for resource allocation and signal decoding order.
**Industry 5.0.** The authors in [137] propose an LLM-based IoT system using open-source LLMs
deployed in a local network environment. The system includes a prompt management module,
a post-processing module, and a task-specific prompts database to address concerns related to
data privacy and security, system scalability, and to enhance the capabilities of the LLM through
integrated prompting methods. The authors in [111] propose SAGE, a smart home agent with
grounded execution, which employs a scheme where a user request initiates a sequence of discrete
actions controlled by an LLM. SAGE manages this process through a dynamically constructed
tree of LLM prompts, which guide the agent in determining the next action, assessing the success
of each action, and deciding when to terminate the process. The authors in [112] present an
edge-based distributed learning architecture in which a large-scale road network is divided into
multiple subgraphs, with data and tasks assigned to individual RSUs. To efficiently learn from this
network, they propose LSGLLM, an LLM-based method that incorporates a spatio-temporal module
to capture spatio-temporal correlations. LSGLLM addresses the absence of spatio-temporal features
in traditional LLMs. The authors in [114] explore the integration of LLMs with the Internet of Senses
technology. In this approach, an edge agent employs an LLM to generate WebXR code, enabling
the visualization of corresponding 3D virtual objects on head-mounted devices and estimating
multi-sensorial media data. CASIT [159] integrates LLMs into IoT systems to enhance the efficiency
and intelligence of data processing and operations. By employing collective intelligence, CASIT
utilizes multiple LLMs for data analysis and anomaly detection. It generates reports through a
step-by-step summary and classification mechanism.


**5.2** **Question Answering / Natural Language Generation (QA/NLG)**

The integration of Large Language Models (LLMs) into MASs has significantly advanced the
capabilities of question answering and natural language generation. There are several prominent frameworks currently developed by leading technology companies, each employing unique
mechanisms to facilitate agent collaboration in practical applications:
**OpenAI’s Swarm Framework** [4] : this framework introduces a novel approach to orchestrating
multiple agents through the concepts of routines and handoffs. In this framework, an agent is
defined as an entity that encompasses specific instructions and tools that are capable of transferring
an active conversation to another agent, a process termed a "handoff." This mechanism allows for
seamless transitions between agents, each specialized in particular tasks, thereby enhancing the
system’s overall efficiency and adaptability. Swarm’s design emphasizes lightweight coordination
and execution, making it suitable for scalable, real-world applications. An example with customer
service focuses on sales and refunds is illustrates in the diagram 7, demonstrating the feasibility of
using Swarm in pratical application.
**Microsoft’s Magentic-One System** [5] : this is a generalist MAS designed to address complex tasks
across diverse domains. At its core is the Orchestrator agent, which is responsible for high-level
planning, progress tracking, and dynamic re-planning to recover from errors. The Orchestrator
delegates specific tasks to specialized agents, such as operating a web browser, navigating local
files, or writing and executing Python code. This modular architecture allows for the integration of
various skills, facilitating the system’s adaptability to a wide range of scenarios.


[4Refer to OpenAI Cookbook at https://cookbook.openai.com/examples/orchestrating_agents](https://cookbook.openai.com/examples/orchestrating_agents)
[5https://www.microsoft.com/en-us/research/articles/magentic-one-a-generalist-multi-agent-system-for-solving-](https://www.microsoft.com/en-us/research/articles/magentic-one-a-generalist-multi-agent-system-for-solving-complex-tasks/)
[complex-tasks/](https://www.microsoft.com/en-us/research/articles/magentic-one-a-generalist-multi-agent-system-for-solving-complex-tasks/)


Multi-Agent Collaboration Mechanisms: A Survey of LLMs 25


Fig. 7. OpenAI’s Swarm use case of customer service.


**IBM’s Bee Agent Framework** [6] : This open-source framework facilitates the development and
deployment of scalable, multi-agent workflows. It provides a foundation for building applications
where multiple AI agents, powered by LLMs such as IBM Granite and Llama 3, collaborate to
achieve complex goals. The framework offers a modular design with prebuilt components for
agents, tools, memory management, and instrumentation. Notably, Bee supports the serialization
of agent states, enabling the pausing and resuming of complex workflows without data loss. It
emphasizes modularity, extensibility, and production-level control to create sophisticated MASs for
a wide range of applications, with future development aimed at enhanced multi-agent orchestration.
**LangChain Agents** [7] : LangChain offers a framework for developing applications powered by
language models, with a particular focus on agents. These agents are designed to interact with
their environment, using tools to process information. LangChain provides a suite of tools and
integrations that facilitate the creation of agents capable of complex reasoning and decision-making
processes. This framework supports the development of sophisticated applications that leverage
the capabilities of LLMs for advanced question answering and natural language generation tasks.
These frameworks represent significant efforts in the field of multi-agent collaboration for
formulating a generalized structure for building multi-agent applications, particularly in the context
of question answering and natural language generation. By allowing specialized agents to work
in concert, they improve the efficiency and effectiveness of AI systems, paving the way for more
sophisticated and adaptable applications.
Another trend in this area of MAS applications for QA/NLG is the introduction of novel frameworks for evaluating responses given by agents and LLMs, which reflects a reimagination of how a
task should be judged - compared to the prevalently existing evaluation approach by using more
capable models to give ratings, or crowd-sourced AI benchmarking from human preference [25].
For example, "Agent-as-a-Judge" formulates a novel framework for evaluating agentic systems software agents powered by LLMs - in natural language generation and question answering [165].
The core concept involves using agentic systems to assess other agentic systems, providing detailed
feedback throughout the task-solving process, and mirroring human evaluation but at a significantly reduced cost and time. The system employs a role-based strategy where specialized agent
modules (e.g., graph construction, code retrieval) operate independently in a decentralized manner
with distinct functionalities, contributing to the overall evaluation. Experiments demonstrate that
Agent-as-a-Judge aligns closely with human expert evaluations and surpasses the performance of
traditional LLM-as-a-Judge methods, especially in complex scenarios, on the DevAI benchmark
with 55 realistic AI development tasks. Another framework, "Benchmark Self-Evolving", leverages


[6https://i-am-bee.github.io/bee-agent-framework/#/](https://i-am-bee.github.io/bee-agent-framework/#/)
[7https://python.langchain.com/docs/tutorials/agents/](https://python.langchain.com/docs/tutorials/agents/)


26 Tran et al.


a MAS to modify existing benchmark instances by altering contexts or questions, thereby creating
new, challenging instances that extend the original benchmarks [129]. It employs the role-based
strategy, with each agent having a specific function (e.g., instance pre-filter, creator and verifier,
candidate option formulator). Experiments conducted on mathematical, logical and commonsense
reasoning demonstrate that the self-evolving benchmarks are more challenging than the original
ones, thus offering a more accurate assessment of LLMs’ true capabilities and limitations, while
also addressing issues like data contamination.
The issue of lacking data for LLM training can be alleviated by synthetic data, in which adopting
MAS is considered a new approach for such task of NLG. Orca-AgentInstruct [8] (formerly AgentInstruct), a novel agentic solution for generating high-quality synthetic data, uses a multi-agent
framework to create tailored datasets from raw data sources, enabling a "generative teaching"
approach for improving model capabilities in different areas [88]. Ultilizing 3 distinct agentic
flows (Content Transformation, Seed Instruction Generation, and Instruction Refinement) and
decentralised structure of agents in each flow, it showed significant performance gains when used
to fine-tune a Mistral 7B model, achieving improvements of up to 54% across various benchmarks.
Orca-AgentInstruct project represents a significant step towards building a synthetic data factory
for model customization and continuous improvement.
In summary, the capabilities of QA/NLG in different tasks have been improved by integrating the
MAS mechanism into the process. Response evaluation in QA is now done with higher confidence,
since the MAS evaluation systems resemble the process of human evaluation and now includes
more dynamic evaluation with automated modified benchmarks. The NLG task of synthesizing
the data is also carried out with higher-quality training data generated from the collaboration
mechanism. Several notable frameworks recently introduced by big-tech companies also pave
the way for the easier creation of MASs, promoting the development of such systems in practical
applications. It is important to recognize that these early efforts are still in the process of being
adapted and that the efficacy of applying them in practice will take time to be assessed. In addition,
the integration of different types and strategies of collaboration, communication structures, and
orchestration architecture also need to be considered, since most existing frameworks or systems
are focusing primarily on role-based strategy and either centralized or decentralized structures.


**5.3** **Social and Cultural Domains**

Research on LLMs and MASs has showcased the capability and applicability of these systems to
simulate human behaviors, social dynamics, and cultural interactions, offering novel methodologies
for understanding complex societal phenomenons, as illustrated in Fig. 8. Studies such as [3, 11]
argue the potential of LLMs to enhance traditional social science methods, including survey research,
online experiments, automated content analyses, and agent-based modeling. However, these studies
also underscore critical limitations, such as biases in training data that lack global psychological
diversity, cautioning against treating stand-alone LLMs as universal solutions. The shift from
stand-alone LLMs to Multi-Agent Collaborative Systems can not only enable the analysis of LLMs
in replicating individual social behavior but also provide powerful tools for exploring complex
social dynamics, collaborative problem-solving, and emergent collective behaviors [46].
Several studies have focused on simulating social interactions through carefully designed environments, where agents are equipped with diverse prompts or LLMs tailored to specific roles. For
instance, [89] follows the definition of social interaction as a theatrical performance, with agents
assuming roles (e.g., office employees or family members) driven by LLMs like GPT-4, Qwen2.5-14b,


[8https://www.microsoft.com/en-us/research/blog/orca-agentinstruct-agentic-flows-can-be-effective-synthetic-data-](https://www.microsoft.com/en-us/research/blog/orca-agentinstruct-agentic-flows-can-be-effective-synthetic-data-generators/)
[generators/](https://www.microsoft.com/en-us/research/blog/orca-agentinstruct-agentic-flows-can-be-effective-synthetic-data-generators/)


Multi-Agent Collaboration Mechanisms: A Survey of LLMs 27















Fig. 8. LLM-based multi-agent collaborative system in social & cultural applications.


or Llama-3-8b. These roles include specific goals, such as providing and receiving feedback during
office discussions. Research has shown that collaboration among LLM-based agents can elicit
human-like capabilities, including conversational skills, theory of mind (reasoning about others’
mental states) [2, 75], Hobbesian social contract theory (submit to authority to avoid chaos) [31],
and non-verbal action inference [79, 147].
**Social Applications.** Authors in [5, 36] suggest that LLM-based agents can replace human
participants in specific social science experiments, while [88] demonstrates their use in generating
diverse natural language data with iterative cross-agent refinement. Moreover, multimodal AI
systems such as those described in [144] integrate verbal, non-verbal, and social cues as input
to multi-tier collaborative agents to generate in-situ suggestions via augmented reality glasses.
Integrating LLM-based agents into traditional agent-based modeling [48] can enhance the realism
of simulations, offering controlled environments to test social theories, including the effects of
policy interventions [10, 148] and norm violation detection [53].
**Cultural Applications.** LLM-based MASs can represent diverse cultural perspectives, advancing
cross-cultural understanding and reducing bias. For example, the CulturePark framework [73]
simulates cross-cultural interactions, with each agent embodying distinct cultural viewpoints.
Similarly, Mango [94] iteratively extracts high-quality cultural knowledge from LLM-based agents,
providing a rich dataset for fine-tuning models to improve their ability to align with diverse cultural
contexts. Another emerging area involves simulating cultural evolution within LLM populations.
By modeling how cultural information is transmitted and transformed among agents, researchers
gain insights into both human cultural dynamics and their influence on LLM behavior [103, 126].
Another area of application involves simulating cultural evolution within LLM populations. By
modeling how cultural information is transmitted and transformed among agents, researchers gain
insights into both human cultural dynamics and their influence on LLM behavior [103].
Despite their promise, LLMs are not perfect replicas of humans and cannot fully replicate the
complexities of human social and cultural behavior. For instance, [36] highlights the limitations
of using LLMs as human replacements in social science experiments, particularly in scenarios
involving information asymmetry (unequal access to private mental states or goals) [161], and in
tasks requiring competition and conflict resolution [89]. To address these challenges, consistent and
standardized benchmarking approaches are necessary to evaluate the cultural and social awareness
of LLM-based agents [109].


28 Tran et al.


**6** **Open Problems & Discussion**


**6.1** **The Road to Artificial Collective Intelligence**
