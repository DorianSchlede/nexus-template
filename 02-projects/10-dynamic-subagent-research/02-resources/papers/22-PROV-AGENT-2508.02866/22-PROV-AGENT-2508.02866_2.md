<!-- Source: 22-PROV-AGENT-2508.02866.pdf | Chunk 2/2 -->


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


