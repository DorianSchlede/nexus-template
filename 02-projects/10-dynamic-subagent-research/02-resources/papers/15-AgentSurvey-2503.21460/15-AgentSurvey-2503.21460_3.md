<!-- Source: 15-AgentSurvey-2503.21460.pdf | Chunk 3/10 -->


7


by identifying and addressing errors. For instance, SELFREFINE [89] applies iterative self-feedback to improve generated responses without external supervision. In reasoning
tasks, STaR [90] and V-STaR [91] train models to verify and
refine their own problem-solving processes, reducing reliance
on labeled data. Additionally, self-verification techniques
enable models to retrospectively assess and correct their
outputs, leading to more reliable decision-making [92].
These approaches collectively enhance LLM agents’ ability
to self-reflect and self-correct, reducing hallucinations and
improving reasoning quality.
_**Self-Rewarding and Reinforcement Learning.**_ Self-rewarding
and reinforcement learning approaches enable LLMs to
enhance performance by generating internal reward signals.
Self-generated rewards help models refine decision-making,
with techniques ensuring stable and consistent learning
improvements [93]. Contrastive distillation further enables
models to align themselves through self-rewarding mechanisms [94]. Additionally, RLC [95] leverages the evaluationgeneration gap via reinforcement learning strategies, facilitating self-improvement. These methods enhance LLM
adaptability by integrating self-rewarding strategies and
reinforcement learning paradigms.


_2.3.2_ _Multi-Agent Co-Evolution_


Multi-agent co-evolution enables LLMs to improve through
interactions with other agents. This involves cooperative
learning, where agents share information and coordinate
actions, as well as competitive co-evolution, where agents
engage in adversarial interactions to refine strategies and
enhance performance.
_**Cooperative and Collaborative Learning.**_ Multi-agent collaboration enhances LLMs by enabling knowledge sharing,
joint decision-making, and coordinated problem-solving.
For instance, ProAgent [96] enables LLM-based agents
to adapt dynamically in cooperative tasks by inferring
teammates’ intentions and updating beliefs, enhancing zeroshot coordination. CORY [97] extends RL fine-tuning into a
cooperative multi-agent framework, where LLMs iteratively
improve through role-exchange mechanisms, enhancing
policy optimality and stability. CAMEL [25] develops a roleplaying framework where communicative agents collaborate
autonomously using inception prompting, improving coordination and task-solving efficiency in multi-agent settings.
These approaches contribute to more efficient, adaptable, and
intelligent multi-agent LLM systems.
_**Competitive and Adversarial Co-Evolution.**_ Competitive coevolution strengthens LLMs through adversarial interactions,
debate, and strategic competition. For example, Red-team
LLMs [98] dynamically evolve in adversarial interactions,
continuously challenging LLMs to uncover vulnerabilities
and mitigate mode collapse, leading to more robust safety
alignment. Du et al. propose a multi-agent debate framework [82] to enhance reasoning by having multiple LLMs
critique and refine each other’s arguments over multiple
rounds, improving factuality and reducing hallucinations.
Furthermore, the MAD framework [99] structures debates
among agents in a tit-for-tat manner, encouraging divergent
thinking and refining logical reasoning in complex tasks.
These competitive co-evolution strategies drive LLMs to


Fig. 3: An overview of evaluation benchmarks and tools
for LLM agents. The left side shows various evaluation
frameworks categorized by general assessment, domainspecific evaluation, and collaboration evaluation. The right
side illustrates tools used by LLM agents, tools created by
agents, and tools for deploying agents.


develop stronger reasoning, resilience, and strategic adaptability in a multi-agent adversarial manner.


_2.3.3_ _Evolution via External Resources_
External resources enhance the evolution of agents by
providing structured information and feedback. Knowledgeenhanced evolution integrates structured knowledge to
improve reasoning and decision-making, while external
feedback-driven evolution leverages real-time feedback from
tools and environments to refine model performance.
_**Knowledge-Enhanced Evolution.**_ LLMs can evolve by integrating structured external knowledge, improving reasoning,
decision-making, and task execution. For example, KnowAgent [83] improves LLM-based planning by integrating action
knowledge, constraining decision paths, and mitigating hallucinations, leading to more reliable task execution. The world
knowledge model (WKM) [84] enhances agent planning
by synthesizing expert and empirical knowledge, providing
global priors and dynamic local knowledge to guide decisionmaking. These approaches collectively improve the evolution
of LLM by incorporating diverse and structured external
information.
_**External Feedback-Driven Evolution.**_ LLMs can refine their
behavior by leveraging external feedback from tools, evaluators, and humans to improve performance iteratively.
For example, CRITIC [100] allows LLMs to validate and
revise their outputs through tool-based feedback, improving
accuracy and reducing inconsistencies. STE [101] enhances
tool learning by simulating trial-and-error, imagination, and
memory, enabling more effective tool use and long-term
adaptation. SelfEvolve [102] adopts a two-step framework
where LLMs generate and debug code using feedback from
execution results, enhancing performance without human
intervention. These approaches enable LLMs to evolve
iteratively by integrating structured feedback, improving
adaptability and robustness.


**3** **EVALUATION AND TOOLS**


As LLM agents continue to evolve in complexity and
capability, robust evaluation frameworks and specialized



8


tools have become essential components of the agent ecosystem. This section explores the comprehensive landscape of
benchmarks, datasets, and tools that enable the development,
assessment, and deployment of LLM agents. We first examine
evaluation methodologies in Section 3.1, covering general
assessment frameworks, domain-specific evaluation systems,
and collaborative evaluation approaches. We then discuss the
tools ecosystem in Section 3.2, including tools used by LLM
agents, tools created by agents themselves, and infrastructure
for deploying agent systems.


**3.1** **Evaluation Benchmarks and Datasets**


The evolution of LLM agents has driven the creation of
specialized benchmarks that systematically evaluate agent
capabilities across technical dimensions and application
domains. These frameworks address three key requirements:
general assessment frameworks, domain-specific scenario
simulation, and collaborative evaluation of complex systems.


_3.1.1_ _General Assessment Frameworks_

The evolution of intelligent agents requires evaluation
frameworks to move beyond simple success-rate metrics
to comprehensive cognitive analysis. Recent advances focus
on building adaptive and interpretable assessment systems
capable of capturing the subtle interplay between reasoning
depth, environmental adaptability, and task complexity.
_**Multi-Dimensional Capability Assessment.**_ Modern benchmarks are increasingly adopting a hierarchical paradigm
that dissects agent intelligence across various dimensions
of reasoning, planning, and problem solving. AgentBench

[124] builds a unified test field across eight interactive
environments, revealing the advantages of a commercial
LLM in complex reasoning. Mind2Web [125] extends this
paradigm to web interaction scenarios, proposing the first
generalist agent for evaluating 137 real-world websites with
different tasks spanning 31 domains. This open environment
benchmark enables multi-dimensional capability assessment
through real web-based challenges. This is in line with
MMAU [126], which enhances explainability through granular capability mapping and breaks down agent intelligence
into five core competencies by more than 3,000 cross-domain
tasks. BLADE [127] extends evaluation to scientific discovery
by tracking the analytical decision patterns of expert validation workflows. VisualAgentBench [128] further extends
this approach to multimodal foundation agents, establishing
a unified benchmark across materialized interactions, GUI
operations, and visual design tasks, and rigorously testing
the LLM’s ability to handle the dynamics of the complex
visual world. Embodied Agent Interface [129] introduces
modular inference components (object interpretation, subobject decomposition, etc.) to provide fine-grained error
classification for embedded systems. CRAB [130] offers
cross-platform testing with graphics-based assessment and
a unified Python interface. These frameworks emphasize
the shift from a single measure of success to multifaceted
cognitive analysis.
_**Dynamic and Self-Evolving Evaluation Paradigms.**_ Nextgeneration framework addresses baseline obsolescence
through adaptive generation and human-AI collaboration.
BENCHAGENTS [131] automatically creates benchmarks


through LLM agents for planning, validating, and measuring
designs, enabling rapid capacity expansion. Benchmark
self-evolving [132] introduces six refactoring operations to
dynamically generate test instances for short-cut biases.
Revisiting Benchmark [133] proposed TestAgent with reinforcement learning for domain adaptive assessment. Other
methods such as Seal-Tools [134] (1,024 nested instances of
tool calls) and CToolEval [135] (398 Chinese APIs across 14
domains), complement static datasets and standardize tool
usage evaluation.


_3.1.2_ _Domain-Specific Evaluation System_


The increasing specialization of agent applications requires
evaluation systems tailored to domain-specific knowledge
and environmental constraints. Researchers are developing
dual-axis frameworks that combine vertical competency
testing for professional scenarios with horizontal validation
in real-world simulated environments.
_**Domain-Specific Competency Tests.**_ Several key application
areas are specifically benchmarked with scenario-driven
assessments. For example, healthcare applications are rigorously tested by MedAgentBench [136] and AI Hospital [137].
Specifically, MedAgentBench contains tasks designed by 300
clinicians in an FHIR-compliant environment, while the AI
hospital simulates clinical workflows through multi-agent
collaboration. The autonomous driving system benefits from
LaMPilot [138], which connects the LLM to the autonomous
driving architecture through code generation benchmarks.
Data science capabilities are evaluated by DSEval [139]
and DA-Code [140], covering lifecycle management from
data debate to model deployment, while DCA-Bench [141]
evaluates dataset curation agents based on real-world quality
issues. TravelPlanner [142] provides a sandbox environment
for travel planning scenarios. It contains 1225 planning
tasks that require multi-step reasoning, tool integration,
and constraint balancing under realistic conditions (e.g.,
budget and time). Machine learning engineering capabilities,
measured by MLAgant-Bench [143] and MLE-Bench [144],
simulate kaggle-like challenges that require optimization of
an end-to-end pipeline. Security-focused AgentHarm [145]
curated 440 malicious agent tasks in 11 hazard categories,
and systematically assessed LLM abuse risk for the first time
in a multi-step tool usage scenario. These domain-specific
benchmarks reveal significant performance gaps compared
to general testing in practical applications.
_**Real-World Environment Simulation.**_ Several benchmarks
bridge the simulation to reality gap with real interactive
environments. OSWorld [146] builds the first scalable realcomputer ecosystem that supports 369 multi-application
tasks across Ubuntu/Windows/macOS. TurkingBench [147]
evaluates 158 micro-tasks using a crowdsourcing-derived
HTML interface, and LaMPilot [138] introduces an executable
code generation benchmark for autonomous driving scenarios. OmniACT [148] provides 32K web/desktop automation
instances with basic requirements for visualization. EgoLife

[149] advances real-world simulation through a 300-hour
multimodal egocentric dataset capturing daily human activities (e.g., shopping, cooking, socializing), paired with EgoLifeQA tasks that test agents’ long-term memory retrieval,
health habit monitoring, and personalized recommendation



9


capabilities in dynamic environments. GTA [150] further
integrates real-world deployed tools and multi-modal inputs
(images, web pages) to evaluate real-world problem-solving
capabilities.


_3.1.3_ _Collaborative Evaluation of Complex Systems_

As agency systems evolve toward organizational complexity,
evaluation frameworks must quantify emergent coordination
patterns and collective intelligence. Recent approaches shift
evaluation from isolated agent proficiency to system-level
cognitive collaboration, revealing scalability challenges in
multi-agent workflows.
_**Multi-Agent System Benchmarking.**_ TheAgentCompany

[151] pioneered enterprise-level assessments using simulated
software company environments to test web interaction and
code collaboration capabilities. Comparative analysis like
AutoGen and CrewAI [152] establishes methodological standards through ML code generation challenges. Large Visual
Language Model Survey [153] systematizes over 200 multimodal benchmarks. For multi-agent collaboration, MLRB

[154] designs 7 competition-level ML research tasks, and
MLE-Bench [144] evaluates Kaggle-style model engineering
through 71 real-world competitions. These efforts collectively
establish rigorous evaluation protocols for emergent agent
coordination capabilities.


**3.2** **Tools**


Tools are an important part of LLM agents. When dealing
with complex tasks, LLM agents can call on external tools to
generate more precise answers. Depending on their creativity,
they can also create tools to solve tasks. In addition, LLM
agents need corresponding tools for deployment, maintenance, and data acquisition.


_3.2.1_ _Tools used by LLM agents_

Since LLM agents do not perform well in handling some
specific tasks, such aas those requiring real-time information
and accurate calculations, external tools are introduced to
help the LLM agents perform these tasks more effectively.
These external tools can be categorized into three main
groups.
_**Knowledge Retrieval.**_ For those real-time information that
LLM agents are not aware of, knowledge retrieval tools, such
as search engines, can help LLM agents to quickly access
up-to-date knowledge so that they are no longer limited to
the knowledge base they had during training. WebGPT [155]
successfully combines online search engines and LLMs with
the incorporation of the commercial API [1] . WebCPM [156],
inspired by WebGPT, develops a web search interface and
uses it to construct the first Chinese long-form question
answer (LFQA) dataset. ToolCoder [157] uses DuckDuckgo [2]

as the search engine for those frequently used public libraries
and employs the BM25 [158] score for those less-known or
private libraries.
_**Computation.**_ LLM agents may suffer hallucinations when
dealing with tasks requiring precise computation. Computational tools like Python interpreters and math calculators


1. https://www.microsoft.com/en-us/bing/apis/bing-web-searchapi

2. https://duckduckgo.com


10



can help LLM agents with complex code execution or computational tasks. AutoCoder [159] designs a dataset with the
interaction with coding execution results to facilitate LLMbased code generation. RLEF [160] improves code generation
performance through an end-to-end reinforcement learning
framework that enables LLMs to learn feedback from code
executors. CodeActAgent [161] is an automatic agentic
system which can update the actions based on the interaction
with the code interpreter. Toolformer [162] integrates a
range of tools, including calculators, to significantly improve
the performance of models in tasks such as mathematical
calculations without compromising the model’s generality.
ART [163] enables LLM to invoke external tools, such
as calculators, when solving complex tasks and excels in
mathematical reasoning and complex computational tasks.
_**API Interactions.**_ Building on external APIs, such as REST
APT, can enable LLM agents to call external services and
extend their functionality, such as manipulating databases
and implementing end-to-end automated processes. RestGPT [164] explores more realistic scenarios by combining
LLM with RESTful APIs and presents RestBench to evaluate the performance of RestGPT. GraphQLRestBench [165]
builds a dataset consisting of sequences of natural language
statements, and function calls to review existing open-source
LLMs, exploring the capabilities of LLMs for API calls.


_3.2.2_ _Tools created by LLM agents_

Since the users of traditional tools tend to be humans,
LLM agents often have limitations when making calls. In
addition, the limitations of existing tools make it difficult
to effectively handle new problems. In recent years, many
studies have explored how LLM agents can create their
tools. CRAFRT [166] provides a flexible framework for tool
creation and retrieval by collecting GPT-4 code solutions
for specific tasks and abstracting them into code snippets
to create specialized tool sets for the tasks. Toolink [167]
performs task resolution by creating a toolset and then
integrating the planning and invocation of tools through a
Chain of Solutions (CoS) approach. CREATOR [168] proposes
a four-phase framework–Creation, Decision, Execution, and
Reflection–to enable LLM agents to create tools and improve
the robustness of the output. LATM [169] proposes a twostage framework that allows LLMs to act as tool makers
and tool users, respectively and proposes a tool caching
mechanism that improves the efficiency of task solving and
reduces the cost while maintaining performance by assigning
different models to different tasks with different levels of
difficulty.


_3.2.3_ _Tools for deploying LLM agents_

LLM tools are essential for the deployment, development,
operation, and maintenance of LLM agents and for the secure
transmission of data. According to their role, these tools can
be categorized into three types.
_**Productionization.**_ The main purpose of the productionization tools is to make it easy for users to deploy LLM
agents in production environments. AutoGen [26] is an
open-source framework that enables developers to build
LLM applications with customizable, conversational multiple
agents. LangChain [170] is an open-source framework for



































Fig. 4: An overview of real-world issues in LLM agent
systems, organized into three domains: security challenges
(including agent-centric and data-centric threats), privacy
concerns (covering memorization vulnerabilities and intellectual property exploitation), and social impact considerations
(highlighting both benefits and ethical challenges).


building LLM applications that is highly extensible and allows users to create custom modules and workflows to meet
their specific needs. LlamaIndex [171] is a data framework
serving large model applications, allowing users to build
LLM applications based on local data. It also provides a
rich toolbox for accessing and indexing data, retrieving and
reordering, and building custom query engines. Dify [172] is
an open-source LLM application development platform that
differs from other platforms in that it allows users to build
and test powerful AI workflows on canvas.
_**Operation and Maintenance.**_ After deploying LLM agents,
the O&M tool ensures that the model performs well during training and remains reliable during production. Ollama [173] is a platform for building LLM agents that also
offers observability and monitoring support, allowing teams
to track their models’ performance in real-time. Dify [172]
enables users to monitor and analyze application logs and
performance over time, allowing for continuous improvements in prompts, datasets, and models based on production
data and annotations.
_**Model Context Protocol.**_ MCP [3] is an open protocol that
standardizes how applications provide context to LLMs.
It is used to create secure links between LLMs and data
sources as well as to build LLM agents and workflows. MCPAgent [174] is a simple framework to build agents using
MCP. As more services become MCP-aware, users will be
able to take full advantage of them.


**4** **REAL-WORLD ISSUES**


As LLM agents become increasingly integrated into various
aspects of society, they bring forth significant real-world
challenges that must be addressed for responsible deployment. Figure 4 provides an overview of these challenges,
categorized into three primary domains: security, privacy,
and social impact. Security concerns encompass both agentcentric threats (Section 4.1) that target model components and
data-centric threats (Section 4.2) that contaminate input data.
Privacy issues (Section 4.3) include memorization vulnerabilities and intellectual property exploitation. Beyond technical


3. https://modelcontextprotocol.io/introduction


concerns, LLM agents raise important ethical considerations
and have broad societal implications (Section 4.4), including
both potential benefits and risks to society. Understanding
these challenges is crucial for developing robust, trustworthy
agent systems.


**4.1** **Agent-centric Security**


Agent-centric security targets defending different types
of attacks on the agent models, where attacks aim to
manipulate, tamper, and steal critical components of the
weights, architecture, and inference process of the agent
models. These agent-centric attacks may lead to performance degradation, maliciously manipulated outputs, and
privacy leaks within agent systems. Li et al. [175] analyze
the security vulnerabilities of LLM agents under attacks
categorized by threat actors, objectives, entry points, and
so on. They also conduct experiments on certain popular
agents to demonstrate their security vulnerabilities. Agent
security bench [176] introduces a comprehensive framework
to evaluate attacks and defenses for LLM-based agents
across 10 scenarios, 10 agents, 400+ tools, 23 attack/defense
methods, and 8 metrics, revealing significant vulnerabilities
and limited defense effectiveness of current LLM agents.
We summarize the agent-centric security issues in the blow
categories.


_4.1.1_ _Adversarial Attacks and Defense_

Adversarial attacks aim to compromise the reliability of the
agents, rendering them ineffective in specific tasks. Mo et
al. [177] categorize adversarial attacks into three components,
i.e., _Perception, Brain, and Action_ . AgentDojo [178] provides an
evaluation framework designed to measure the adversarial
robustness of AI agents by testing them on 97 realistic tasks
and 629 security test cases. ARE [179] evaluates multimodal
agent robustness under adversarial attacks. For adversarial
attack methods, CheatAgent [180] uses an LLM-based agent
to attack black-box LLM-empowered recommender systems
by identifying optimal insertion positions, generating adversarial perturbations, and refining attacks through iterative
prompt tuning and feedback. GIGA [181] introduces generalizable infectious gradient attacks to propagate adversarial
inputs across multi-agent, multi-round LLM-powered systems by finding self-propagating inputs that generalize well
across contexts. For adversarial attacks defense methods,
LLAMOS [182] introduces a defense technique for adversarial attacks by purifying adversarial inputs using agent
instruction and defense guidance before they are input into
the LLM. Chern et al. [183] introduce a multi-agent debate
method to reduce the susceptibility of agents to adversarial
attacks.

