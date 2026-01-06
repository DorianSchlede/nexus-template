<!-- Source: 03-PROV-AGENT_Unified_Provenance_for_AI_Agents.pdf | Chunk 1/1 -->

# PROV-AGENT: Unified Provenance for Tracking AI Agent Interactions in Agentic Workflows

Renan Souza _[∗]_, Amal Gueroudji _[†]_, Stephen DeWitt _[‡]_, Daniel Rosendo _[∗]_, Tirthankar Ghosal _[∗]_,
Robert Ross _[†]_, Prasanna Balaprakash _[§]_, Rafael Ferreira da Silva _[∗]_

_∗_ National Center for Computational Sciences, Oak Ridge National Lab, Oak Ridge, TN, USA

_†_ Mathematics and Computer Science Division, Argonne National Laboratory, Lemont, IL, USA

_‡_ Computational Sciences and Engineering Division, Oak Ridge National Lab, Oak Ridge, TN, USA
_§_ Computer Science and Mathematics Division, Oak Ridge National Lab, Oak Ridge, TN, USA



_**Abstract**_ **—Large Language Models (LLMs) and other founda-**
**tion models are increasingly used as the core of AI agents. In**
_**agentic workflows**_ **, these agents plan tasks, interact with humans**
**and peers, and influence scientific outcomes across federated and**
**heterogeneous environments. However, agents can hallucinate**
**or reason incorrectly, propagating errors when one agent’s**
**output becomes another’s input. Thus, assuring that agents’**
**actions are transparent, traceable, reproducible, and reliable is**
**critical to assess hallucination risks and mitigate their workflow**
**impacts. While provenance techniques have long supported these**
**principles, existing methods fail to capture and relate agent-**
**centric metadata such as prompts, responses, and decisions with**
**the broader workflow context and downstream outcomes. In this**
**paper, we introduce PROV-AGENT, a provenance model that**
**extends W3C PROV and leverages the Model Context Protocol**
**(MCP) and data observability to integrate agent interactions into**
**end-to-end workflow provenance. Our contributions include: (1) a**
**provenance model tailored for agentic workflows, (2) a near real-**
**time, open-source system for capturing agentic provenance, and**
**(3) a cross-facility evaluation spanning edge, cloud, and HPC**
**environments, demonstrating support for critical provenance**
**queries and agent reliability analysis.**
_**Index Terms**_ **—Workflows, Agentic Workflows, Provenance,**
**Lineage, Responsible AI, LLM, Agentic AI**


I. INTRODUCTION


The integration of foundation models, often referred to as
Large “X” Models (LxMs), into computational workflows is
rapidly advancing across scientific and industrial domains [1].
These models excel in language, vision, time-series, and
robotics tasks, driving innovation in genomics, chemistry, and
manufacturing. This shift has driven the emergence of _agentic_
_workflows_, where autonomous agents make decisions, plan
tasks, and coordinate with humans and other agents. These
agents operate in dynamic environments across heterogeneous
computing platforms, including edge devices, cloud systems,
and high-performance computing (HPC). Unlike traditional


Cite this paper as: R. Souza, A. Gueroudji, S. DeWitt, D. Rosendo, T.
Ghosal, R. Ross, P. Balaprakash, R. F. da Silva, “PROV-AGENT: Unified
Provenance for Tracking AI Agent Interactions in Agentic Workflows,”
Proceedings of the 21st IEEE International Conference on e-Science (eScience), Chicago, IL, USA, 2025.


This manuscript has been authored by UT-Battelle, LLC, under contract DE-AC05-00OR22725 with the US Department


of Energy (DOE). The publisher, by accepting the article for publication, acknowledges that the U.S. Government retains


a non-exclusive, paid up, irrevocable, worldwide license to publish or reproduce the published form of the manuscript, or


allow others to do so, for U.S. Government purposes. The DOE will provide public access to these results in accordance


with the DOE Public Access Plan (http://energy.gov/downloads/doe-public-access-plan).



workflows with static, deterministic paths [2], agentic workflows are non-deterministic, shaped by near real-time data,
adaptive decisions, and evolving interactions [3], [4]. They
often display dynamic, cyclic behavior, where agent outputs
inform subsequent decisions or feedback loops.
Although Artificial Intelligence (AI) agents offer capabilities for automating complex processes, they introduce new
challenges for transparency, reproducibility, and reliability.
They may generate hallucinated or incorrect outputs, especially when relying on generative models, which can propagate
through the workflow, compounding errors and making it difficult to assess the correctness of the results [5]. The risks are
amplified in workflows where agent decisions influence other
agents or downstream tasks, potentially affecting scientific
conclusions or operational outcomes. Provenance data management has long played a central role in providing for such
transparency, reproducibility, and reliability in computational
workflows [6]. However, traditional provenance approaches
are not designed to capture the intrinsic dynamics of modern
AI agents. Provenance data must not only capture the data flow
and task execution history but also represent the reasoning
processes, model invocations, and contextual information that
drive agent decisions. This level of detail enables rigorous
root cause analysis when unexpected or erroneous behavior
occurs. For example, understanding how a surprising result
was produced requires tracing back through multiple agent interactions, prompts, responses, and intermediate computations.
A unified provenance graph that considers AI agent actions
as first-class components, on par with traditional workflow
tasks, enables comprehensive traceability and analysis. This
structure supports critical queries such as: (1) _What specific_
_input data led an agent to make a particular decision?_ (2) _How_
_did an agent’s decision influence the control or data flow_
_within the workflow?_ (3) _Which downstream outputs were_
_affected by a specific agent interaction?_ (4) _Where did erro-_
_neous data originate, and through which agents decisions or_
_workflow tasks did it propagate?_ These questions are essential
for interpreting results, debugging workflows, and improving
agent performance through better prompts and model tuning.
In this paper, we build on foundational efforts in workflow
provenance research to introduce a framework that captures
both traditional workflow metadata and AI agent interac

tions. Our contributions are threefold: (1) **PROV-AGENT**, a
provenance model that extends the W3C PROV [7] standard
and incorporates concepts from the Model Context Protocol
(MCP) [8] to represent agent actions and their connections
to data and workflow tasks; (2) an open-source system [9]
for data observability and runtime agentic provenance capture in workflows; and (3) a preliminary evaluation with a
cross-facility agentic workflow involving edge devices, cloud
services, and HPC systems.


II. BACKGROUND AND RELATED WORK


_A. Provenance for Tracking AI Agents in Dynamic Cross-_
_Facility Workflows_


Agentic workflows are emerging as a new paradigm in
scientific computing, where autonomous AI agents are integrated into complex, multi-step processes. These agents,
often powered by foundation models such as LLMs, take
on responsibilities traditionally handled by humans or static
scripts. They interpret data, make decisions, and adaptively
steer workflow execution. To support the development and
orchestration of such agentic workflows, a variety of frameworks have emerged. For instance, LangChain [10], [11], AutoGen [12], LangGraph [13], Academy [3], and CrewAI [14]
support multi-agent systems that interact through prompt exchanges, calls to foundation models typically hosted by AI
service providers in the cloud (e.g., OpenAI, SambaNova), and
shared context. These frameworks support MCP [8], which
is emerging as a standard in academia and industry. MCP
defines core agentic AI development concepts, including tools,
prompts, resources, context management, and agent–client
architecture that can communicate with external sources, such
as knowledge bases or web pages, for Retrieval-Augmented
Generation (RAG) [15] to dynamically augment prompts.
A growing challenge in these workflows involves managing execution across physically and logically distributed
facilities that include edge devices, cloud services, and HPC
systems [16]–[19] (Fig. 1). Scientific experiments may be conducted in external laboratories or at the edge, generating data
in near real-time. These data must be immediately transmitted
to an HPC system, where they feed into simulations, analytics
pipelines, or machine learning (ML) training processes. This
tight integration requires not only reliable data movement
across sites but also a coherent understanding of how AI agents
interact with this data across systems.
While some MCP-based agent frameworks record prompts,
responses, and AI service invocations, these data are typically
isolated from the rest of the workflow. This disconnection
hinders the contextualization of agent interactions or understanding their downstream impact. Existing provenance
techniques lack explicit representations of key agent artifacts
and their integration with the workflow. They typically model
workflows as static graphs, missing the semantics needed to
capture agentic behavior, dynamic decisions, and model-driven
reasoning. We argue that _agentic provenance_, i.e., provenance
data that track tasks executed by AI agents and their influence
on downstream non-agentic tasks and data in the workflows,



|Experimental Facility<br>Science Labs<br>Edge devices<br>Instruments Robots Sensors<br>AI Agent AI Agent|Live streaming of:<br>- Data<br>- Computation<br>results<br>- Agents’ decisions|HPC Facility<br>Physics Simulations<br>AI Model Training<br>AI Agent AI Agent|Col4|
|---|---|---|---|
|Experimental Facility<br>Science Labs<br>Edge devices<br>AI Agent<br>AI Agent<br>Instruments<br>Robots<br>Sensors|Data<br>Streaming|Data<br>Streaming|Data<br>Streaming|
|||||
|Cloud|Cloud|Cloud|Cloud|


Fig. 1: Agentic workflow spanning an edge-cloud-HPC continuum. Data stream in near real time from the experimental facility to HPC systems, with results feeding back into upstream
tasks. Agentic tasks (tools) run alongside traditional ones,
making provenance critical to trace potential hallucinations or
errors that may propagate through the entire workflow.


provides the glue power needed to unify these elements into a
single, queryable graph. This enables traceability, root cause
analysis, and continuous agent improvement, such as refining
prompts or tuning model parameters to reduce hallucinations,
which are essential in agentic workflows to support responsible, reproducible, and trustworthy AI-driven decisions [6].


_B. W3C PROV and Extensions for Workflows, AI, and Agents_


The W3C PROV standard [7] is a widely adopted representation model for provenance, providing a structured way
to describe how data were produced, by whom, and through
which processes. Fortunately, the W3C PROV standard already
defines **Agent**, the central abstraction in this work, as one
of its three core classes, alongside Entity (data) and Activity
(process), with agents representing either software or human
actors responsible for activities. Fig. 2 shows these core classes
and their main relationships among them.


Fig. 2: The W3C PROV Provenance Model [7].


PROV supports domain- and application-specific extensions
and underpins many workflow provenance systems requiring standardized, interoperable representations of complex
processes. For instance, PROV-DfA [20] extends PROV to
capture human actions in human-steered workflows, while
ProvONE [21] adds workflow-specific metadata and aims
at supporting existing workflow management systems. For





Cross-facility Agentic Workflow


















AI/ML workflows, PROV-ML [22] combines general workflow concepts with ML-specific artifacts, especially for model
training and evaluation. FAIR4ML [23] adopts a model-centric
approach to support the Findability, Accessibility, Interoperability, and Reproducibility (FAIR) principles. These works
are orthogonal to ours, as they define complementary concepts rather than representing AI agents that steer workflows.
Although the W3C PROV has been extended for agents and
multi-agent systems [24], [25], these earlier efforts predate
agentic workflows, lacking support for core agentic AI concepts [26] and how they relate to broader workflow.


III. A PROVENANCE MODEL FOR AGENTIC WORKFLOWS


PROV-AGENT is a provenance model for representing AI
agent interactions, model invocations, and their relationships
to non-agentic tasks and data in agentic workflows (Fig. 3). It
extends W3C PROV and incorporates MCP concepts to unify
agents and traditional components as first-class elements.


Fig. 3: PROV-AGENT: A W3C PROV Extension for Agentic
Workflows. Dashed arrows represent _subClassOf_ .


At its core, the model includes standard workflow structures such as Campaign, Workflow, and _Task_, modeled
as subclasses of PROV Activities. Campaigns are associated with Person or Organization agents via _wasAssociated-_
_With_, omitted from the figure to reduce clutter. Tasks consume (PROV _used_ ) and produce (PROV _generated_ ) domainspecific data objects (DomainData). Typically, in a provenance graph, they contain parameters, arguments, KPIs, QoIs,
and pointers to domain data files or data objects stored
elsewhere [27]. Tasks also generate two additional types
of metadata: SchedulingData and TelemetryData.



SchedulingData contains where the task ran, including details such as compute node, CPU core, or GPU ID.
TelemetryData contains runtime metrics such as CPU and
GPU usage, and disk usage. These data, modeled as subclasses
of DataObject, which is a subclass of PROV Entity, enrich
the provenance graph with infrastructure-level context needed
for traceability and performance analysis.
We extend the abstract W3C PROV **Agent** by modeling
AIAgent as its subclass, enabling a natural integration of
agent actions and interactions into the broader workflow provenance graph. This modeling is not constrained to single-agent
scenarios. Multi-agentic workflows, with other AI agents, each
with their own tools and reasoning paths, can be instantiated
within the same provenance graph, enabling the representation
of collaborative or parallel agent behaviors within a workflow.
Following the MCP terminology, an AI agent can be associated with one or many tool executions (AgentTool)
and each tool may be informed by (PROV _wasIn-_
_formedBy_ ) one or many AIModelInvocations. Each
AIModelInvocation uses a Prompt and a specific
AIModel, which holds model metadata, including its name,
type, provider, temperature, and other parameters, and _gen-_
_erates_ a ResponseData object, which is _attributedTo_ the
corresponding agent. Although LLMs are more common,
the PROV-AGENT is designed to be modality-agnostic and
supports other foundation models, such as those for vision,
audio, or multimodal reasoning, as long as they follow a
prompt-invocation-response interaction model.
The data used or generated by agents, including prompts,
responses, are represented as subclasses of the DataObject
Entity. This allows agents to consume and produce not only
DomainData, but also system-level and contextual data such
as SchedulingData and TelemetryData. When instances of subclasses of DataObject are generated by agent
tools, they are attributed to ( _wasAttributedTo_ ) the instance
of the agent. The additional data types can be used by the
agent as part of reasoning or planning, for example through
RAG strategies to enhance prompts with relevant contextual
knowledge. Since the relationships are explicitly modeled using standard PROV constructs such as _used_, _wasGeneratedBy_,
_wasAssociatedWith_, and _wasInformedBy_, the resulting graph
is fully connected and queryable. This enables users to trace
a final output or decision all the way back through agent
reasoning, prompts, input data, system context, and execution
metadata, addressing the key challenge of capturing agentic
behavior as part of end-to-end workflows.


IV. SYSTEM IMPLEMENTATION AND EVALUATION


_A. Implementation_


Rather than building a new provenance system from scratch,
we extend _Flowcept_ [9], an open-source distributed provenance framework designed for complex, heterogeneous workflows spanning experimental facilities at the edge, cloud
platforms, and HPC environments. Flowcept uses a federated,
broker-based model where raw provenance data, which may
come in varied formats and schemas, can be streamed from


instrumented scripts, data observability hooks in workflow
tools (e.g., Dask, MLflow), and from data streaming services
and storage layers such as Redis, Kafka, SQLite, file systems,
and object stores while the workflows run [18]. A central
consolidation service unifies, curates this data into a persistent
provenance database while applying a W3C PROV-extended
model, making it well-suited for capturing and contextualizing
provenance in end-to-end agentic workflows.


Building on the MCP concepts, when the MCP server is
initialized, we begin by creating a new instance of AIAgent,
assigning it an identifier and name so it can be properly
associated with the tools it executes. Flowcept supports several
instrumentation methods, but for MCP-based tools, the most
straightforward method is via decorators. In generic Python
functions, applying the @flowcept_task decorator ensures
that, upon execution, the function’s inputs, outputs, and any
generated telemetry or scheduling data are automatically captured. Follow this approach, since MCP tools have welldefined input arguments and return values, we introduce a
new decorator, @flowcept_agent_tool, which creates
a corresponding AgentTool execution activity for each
tool execution. This activity is associated with the executing
agent and linked to its inputs and outputs using the PROV
relationships defined in the PROV-AGENT model.


Tool executions are often informed by one or more
AIModel calls. Given our driving use cases and that most
agentic workflow users employ LLMs for their agents, this
first implementation of PROV-AGENT focuses on supporting
LLMs by providing a generic wrapper for abstract LLM
objects, compatible with models from popular LLM interfaces, including CrewAI, LangChain, and OpenAI. Whenever a prompt is sent to an LLM service provider in the
cloud (e.g., OpenAI, SambaNova, Azure), the wrapper captures the prompt, response, model metadata (e.g., provider,
name, and parameters like temperature), and optional telemetry such as response time. Fig. 4 shows an MCP tool example annotated with the decorator and using the wrapper
FlowceptLLM. Model metadata are recorded within an instance of AIModel and each invocation is recorded as an
AIModelInvocation activity and linked to the model,
prompt, and response, according to the defined relationships.
When a tool depends on LLM results, Flowcept establishes
a _wasInformedBy_ relationship from the AgentTool to the
relevant AIModelInvocation activities. While this implementation records only the agent’s ID and name, the model
supports extended metadata, such as model and tools’ version
control state, and further configuration parameters.


Flowcept also provides an MCP agent with a Streamlit GUI
that enables users to interact with the provenance database
through natural language queries at runtime. While the details
of this agent are beyond the scope of this paper, in the next
section we highlight how it helps users to query and explore
the provenance data captured using PROV-AGENT.



1 **from** langchain_openai **import** ChatOpenAI

2 **from** flowcept **import** FlowceptLLM, flowcept_agent_tool


3

4 @mcp.tool()

5 @flowcept_agent_tool

6 **def** evaluate_scores(layer, result, scores):

7 ...

8 prompt = get_prompt(layer, result, scores)

9 llm = FlowceptLLM(ChatOpenAI(model="gpt-4o"))

10 response = llm.invoke(prompt)

11 ...

12 **return** ...


Fig. 4: MCP agent tool that invokes an LLM to
assess physics model outputs. With the decorator
@agent_flowcept_task and FlowceptLLM wrapper,
agent tool and LLM invocation provenance are captured.


_B. Preliminary Evaluation_


In this section, we evaluate PROV-AGENT and its implementation by demonstrating how agent decisions, LLM interactions, and workflow tasks are unified in a single provenance
graph, enabling users to trace erroneous outputs back to their
upstream prompts, inputs, and prior decisions.
**Use case.** We employ PROV-AGENT in an autonomous
additive manufacturing workflow being developed at Oak
Ridge National Laboratory (ORNL) [28]. This envisioned
workflow integrates a metal 3D printer at ORNL’s Manufacturing Demonstration Facility (MDF) on the Edge with an HPC
system at the ORNL Leadership Computing Facility (OLCF),
streaming sensor data in near real-time to HPC simulations,
illustrating a concrete case of the generic workflow in Fig. 1.
Although the direct live data connection between the sensors
and simulation is still under development, our implementation
already applies to the agentic control loop and distributed
facilities at ORNL. At MDF, sensor drivers collect data layer
by layer as a metal component is fabricated. This layer-specific
data are used to estimate the current state of the system. Using
the approach of model predictive control [29], a forwardlooking physics-based model explores the downstream consequences of decisions for upcoming layers. Each prospective
decision for the upcoming layer is scored using an analysis
routine. Researchers are investigating the benefits of using AIdriven decision-making via Analysis Agent tools invoking an
LLM ( _gpt-4o_ ) service hosted in the cloud. The agents use
structured prompts to decide which control result is best for
print control based on their scores and other data in the agent
context, such as previous decisions and user guidance. Thus,
the decision made for each layer informs the decision logic
in the next, enabling the system to learn over the course of a
print. However, because the agent relies on an LLM, there is
a risk of hallucinated or incorrect outputs. Since each decision
influences the next in this iterative loop, a single error may
propagate across layers, potentially compromising downstream
outputs, thus making provenance tracking essential.
**End-to-end Provenance Graph.** Figure 5-A shows how
PROV-AGENT would function in the additive manufacturing
use case. After the scientist inputs the experiment setup, the


Fig. 5: (A) Instantiation of the unified provenance graph using PROV-AGENT for an additive manufacturing workflow. Sensor
drivers run on edge devices, while agents and physics models run on HPC. Sensor data are generated layer by layer and
used by the simulation model to assess print quality. An AI agent analyzes results and makes layer-specific decisions, where
decisions at iteration _i_ influence iteration _i_ +1. Only two iterations are shown, though typical workflows span up to thousands.
Arrows reverse standard W3C PROV directions ( _used_, _wasGeneratedBy_ ) for top-down clarity.
(B) Chat window showing a natural language query to the Flowcept Agent for Query 3.


driver (Sensor_Driver_i) iteratively triggers the sensors
for each printed layer _i_ . The resulting Sensor_Data_i
is streamed to the HPC system for processing by a
physics-based model (Physics_Model_i) and evaluation
task (Model_Evaluation_i), producing control results
and scores. Experiment_Setup, Sensor_Data_i,
Control_Result_i, and Scores_i are modeled as
DomainData, and their linked activities are Tasks.
For every layer _i_, an agent decision-making tool is
executed to assess the scores for physics model predictions, creating an instance (Agent_Tool_i) of the
class AgentTool, and is linked to an instance of the
AIAgent, the Analysis_Agent_i. Every tool execution
for layer _i_ uses the outputs of the physics model and
their evaluation scores, and invokes the cloud-based LLM
models via LLM_Invocation_i, which are instances of
AIModelInvocation. LLM invocations are explicitly connected to the used Prompt_i and generated Response_i
instances, where the responses are attributed to the agent
instance. The resulting agent decisions (Agent_Decision_i),
which are instances of DomainData, are also attributed to
the agent, completing each agentic reasoning cycle.
Several model components from the PROV-AGENT
schema are intentionally omitted from the figure, including Campaign, Workflow, TelemetryData, and
SchedulingData. These classes are recorded in the underlying provenance database but excluded from the visual
representation to reduce clutter. Activities, e.g., workflow tasks
and agent tools, are linked to location metadata indicating
where they ran (e.g., edge, HPC, or cloud). Though omitted in
the figure, these PROV Location entities help map execution
across the Edge–Cloud–HPC continuum.
**Query examples enabled by PROV-AGENT.** With PROVAGENT, several new queries are enabled to support agent
accountability and tracing back when errors/hallucinations
happen. Below we show a few examples of queries using a
distributed Edge-Cloud-HPC workflow that mimics the agentic
additive manufacturing workflow under development.

_•_ **Q1. Given an agent decision, what was the complete**
**lineage until the first input data?**
Given an agent decision Agent_Decision_i, the query
traverses to its generating Agent_Tool_i, then to the
inputs it used: Scores_i, Control_Result_i, and
Agent_Decision_i-1. These are traced back through
Model_Evaluation_i and Physics_Model_i to the
original Sensor_Data_i that was generated by the driver
for layer _i_ when utilized the recorded Experiment_Setup.

_•_ **Q2. When printing layer 2, what was the agent decision,**
**the available score options, and the reasoning behind**
**the decision?**
Starting at Agent_Decision_2, we trace back to
Agent_Tool_2 and inspect the input Scores_2,
Control_Result_2, and the Response_2 from the
LLM_Invocation_2 to understand the reasoning context.

_•_ **Q3. What was the LLM prompt and response when a**
**surprising agent decision was identified?**



Given that a hallucination was identified when the agent
was deciding on the scores for layer 2, after identifying
the unexpected Agent_Decision_2, the query traces back
to Agent_Tool_2 and its linked LLM_Invocation_2 to
retrieve the corresponding Prompt_2 and Response_2.
This query is illustrated in the Streamlit chat GUI of
Flowcept agent in Figure 5-B.

_•_ **Q4. How did an agent decision influence subsequent**
**workflow activities?**
Given that an agent decision Agent_Decision_i is
used by another Agent_Decision_i+1, the query recursively navigates on the used/wasGeneratedBy relationships
in the path between the Agent_Decision_i and the
Agent_Decision in the last layer.

_•_ **Q5. Where did erroneous data originate, and how did it**
**propagate?**
After identifying a faulty Agent_Decision_i, the query
traces backward through the tool, LLM response, model
outputs, and Sensor_Data_i to find the cause, and forward
to identify affected downstream results.
These queries demonstrate how PROV-AGENT enables endto-end analysis of agent behavior within workflows, supporting
accountability, debugging, and iterative improvement.


V. CONCLUSION


As AI agents become core components of workflows, ensuring transparency, accountability, and reproducibility is critical,
especially given their non-deterministic behavior and potential
to hallucinate and propagate errors across data and tasks in the
workflows. PROV-AGENT addresses this need by extending
the W3C PROV standard and leveraging the Model Context
Protocol (MCP) to capture fine-grained agentic provenance.
We build on established provenance foundations to add key AI
agent artifacts, including tools, prompts, responses, and model
invocations, and integrate them to the non-agentic tasks and
data in the workflow. This unified approach not only supports
traceability and root cause analysis but also enables continuous agent improvement through the comparison of decisions
across prompt engineering refinements or fine-tuning of model
parameters. We demonstrated our open-source implementation
in an agentic workflow use case running on distributed facilities with feedback loops and AI agents steering execution.
To the best of our knowledge, this is the first provenance
framework designed to track agent actions and decisions in
agentic workflows. While this is an early step, it establishes a
foundation that researchers and practitioners can build on, not
only to enable root-cause analysis, interpretability, and model
and prompt fine-tuning, but also to explore new techniques
for detecting and ultimately remediating hallucinations in AIdriven decisions.


**Acknowledgments.** The authors thank the ORNL team: Miaosen
Chai, Timothy Poteet, Phillipe Austria, Marshall McDonnell, Ross
Miller, A.J. Ruckman, Tyler Skluzacek, Feiyi Wang, Sarp Oral, Arjun
Shankar for their help with the use case development. ChatGPT-4o
was used to help polish writing, improve conciseness, and check


grammar. This research used resources of the Oak Ridge Leadership
Computing Facility at ORNL, supported by the Office of Science,
U.S. Department of Energy (DOE) under Contract No. DE-AC0500OR22725. Additional DOE support was provided under Contract
No. DE-AC02-06CH11357.


REFERENCES


[1] P. Fettke, H.-G. Fill, and J. K¨opke, “LLM, LAM, LxM Agent: From
Talking to Acting Machines: Insights from the Perspective of Conceptual
Modeling,” _Enterprise Modelling and Information Systems Architectures_
_(EMISAJ)_, vol. 20, 2025.

[2] F. Suter, T. Coleman, [˙] I. Altintas¸, R. M. Badia, B. Balis, K. Chard,
I. Colonnelli, E. Deelman, P. Di Tommaso, T. Fahringer _et al._, “A terminology for scientific workflow systems,” _Future Generation Computer_
_Systems_, p. 107974, 2025.

[3] J. G. Pauloski, Y. Babuji, R. Chard, M. Sakarvadia, K. Chard, and
I. Foster, “Empowering Scientific Workflows with Federated Agents,”
_arXiv preprint arXiv:2505.05428_, 2025.

[4] R. Ferreira da Silva, M. Abolhasani, D. A. Antonopoulos, L. Biven,
R. Coffee, I. T. Foster, L. Hamilton, S. Jha, T. Mayer, B. Mintz _et al._,
“A Grassroots Network and Community Roadmap for Interconnected
Autonomous Science Laboratories for Accelerated Discovery,” _arXiv_
_preprint arXiv:2506.17510_, 2025.

[5] X. Gu, X. Zheng, T. Pang, C. Du, Q. Liu, Y. Wang, J. Jiang, and M. Lin,
“Agent smith: a single image can jailbreak one million multimodal
llm agents exponentially fast,” in _Proceedings of the 41st International_
_Conference on Machine Learning_, ser. ICML’24. JMLR.org, 2024.

[6] R. Souza, S. Caino-Lores, M. Coletti, T. J. Skluzacek, A. Costan,
F. Suter, M. Mattoso, and R. F. Da Silva, “Workflow provenance
in the computing continuum for responsible, trustworthy, and energyefficient ai,” in _2024 IEEE 20th International Conference on e-Science_
_(e-Science)_, 2024.

[7] P. Groth and L. Moreau. (2013) W3C PROV: an overview
of the prov family of documents. [Online]. Available: [https:](https://www.w3.org/TR/prov-overview)
[//www.w3.org/TR/prov-overview](https://www.w3.org/TR/prov-overview)

[[8] “Model context protocol,” https://modelcontextprotocol.io/introduction,](https://modelcontextprotocol.io/introduction)
2025.

[[9] “Flowcept code repository,” https://github.com/ORNL/flowcept, 2025.](https://github.com/ORNL/flowcept)

[10] O. Topsakal and T. C. Akinci, “Creating large language model applications utilizing langchain: A primer on developing llm apps fast,” in
_International Conference on Applied Engineering and Natural Sciences_,
vol. 1, no. 1, 2023, pp. 1050–1056.

[11] B. Auffarth, _Generative AI with LangChain: Build large language model_
_(LLM) apps with Python, ChatGPT, and other LLMs_ . Packt Publishing
Ltd, 2023.

[12] Q. Wu, G. Bansal, J. Zhang, Y. Wu, B. Li, E. Zhu, L. Jiang, X. Zhang,
S. Zhang, J. Liu _et al._, “Autogen: Enabling next-gen llm applications
via multi-agent conversation,” _arXiv preprint arXiv:2308.08155_, 2023.

[13] J. Wang and Z. Duan, “Agent AI with langgraph: A modular framework
for enhancing machine translation using large language models,” _arXiv_
_preprint arXiv:2412.03801_, 2024.

[[14] “CrewAI,” https://www.crewai.com/, 2025.](https://www.crewai.com/)

[15] Y. Gao, Y. Xiong, X. Gao, K. Jia, J. Pan, Y. Bi, Y. Dai, J. Sun,
H. Wang, and H. Wang, “Retrieval-augmented generation for large
language models: A survey,” _arXiv preprint arXiv:2312.10997_, vol. 2,
no. 1, 2023.

[16] S. Murugesan, “The rise of agentic AI: implications, concerns, and the
path forward,” _IEEE Intelligent Systems_, vol. 40, no. 2, pp. 8–14, 2025.

[17] D. B. Acharya, K. Kuppan, and B. Divya, “Agentic ai: Autonomous
intelligence for complex goals–a comprehensive survey,” _IEEE Access_,
2025.

[18] R. Souza, T. J. Skluzacek, S. R. Wilkinson, M. Ziatdinov, and R. F.
da Silva, “Towards lightweight data integration using multi-workflow
provenance and data observability,” in _IEEE International Conference_
_on e-Science_, 2023.

[19] R. Ferreira da Silva, D. Bard, K. Chard, d. W. Shaun, I. T. Foster,
T. Gibbs, C. Goble, W. Godoy, J. Gustafsson, U.-U. Haus, S. Hudson,
S. Jha, L. Los, D. Paine, F. Suter _et al._, “Workflows community summit
2024: Future trends and challenges in scientific workflows,” 2024.

[20] R. Souza and M. Mattoso, “Provenance of dynamic adaptations in usersteered dataflows,” in _Provenance and Annotation of Data and Processes_
_(IPAW)_ . Cham: Springer International Publishing, 2018, pp. 16–29.




[21] Y. Cao, C. Jones, V. Cuevas, M. Jones, B. Lud¨ascher, T. M. McPhillips,
P. Missier, C. R. Schwalm, P. Slaughter, D. Vieglais, L. Walker, and
Y. Wei, “Provone: extending prov to support the dataone scientific
community.”

[22] R. Souza, L. G. Azevedo, V. Lourenc¸o, E. Soares, R. Thiago,
R. Brand˜ao, D. Civitarese, E. Vital Brazil, M. Moreno, P. Valduriez, and
M. Mattoso, “Workflow provenance in the lifecycle of scientific machine
learning,” _Concurrency and Computation: Practice and Experience_,
vol. 34, no. 14, p. e6544, 2022.

[23] L.-J. Castro, D. Garijo, D. Rebholz-Schuhmann, D. Solanki, J. T.
Ciuciu-Kiss, D. Katz, L. Eklund, and G. Bharathy, “FAIR4ML Metadata
[Schema,” https://w3id.org/fair4ml, 2025.](https://w3id.org/fair4ml)

[24] D. B. Davis, J. Featherston, M. Fukuda, and H. U. Asuncion, “Data
provenance for multi-agent models,” in _2017 IEEE 13th International_
_Conference on e-Science (e-Science)_ . IEEE, 2017, pp. 39–48.

[25] S. Friedman, J. Rye, D. LaVergne, D. Thomsen, M. Allen, and K. Tunis,
“Provenance-based interpretation of multi-agent information analysis,”
_arXiv preprint arXiv:2011.04016_, 2020.

[26] R. Sapkota, K. I. Roumeliotis, and M. Karkee, “AI agents vs. Agentic
AI: A conceptual taxonomy, applications and challenges,” _arXiv preprint_
_arXiv:2505.10468_, 2025.

[27] R. Souza, L. Azevedo, R. Thiago, E. Soares, M. Nery, M. A. S. Netto,
E. V. Brazil, R. Cerqueira, P. Valduriez, and M. Mattoso, “Efficient
runtime capture of multiworkflow data using provenance,” in _IEEE_
_eScience_, 2019.

[[28] https://intersect-architecture.readthedocs.io/en/latest/examples/aam/](https://intersect-architecture.readthedocs.io/en/latest/examples/aam/index.html)
[index.html.](https://intersect-architecture.readthedocs.io/en/latest/examples/aam/index.html)

[29] M. Schwenzer, M. Ay, T. Bergs, and D. Abel, “Review on model
predictive control: an engineering perspective,” _The International_
_Journal of Advanced Manufacturing Technology_, vol. 117, no. 5,
[pp. 1327–1349, 2021. [Online]. Available: https://doi.org/10.1007/](https://doi.org/10.1007/s00170-021-07682-3)
[s00170-021-07682-3](https://doi.org/10.1007/s00170-021-07682-3)


