<!-- Source: 02-ContextSurvey-2507.13334.pdf | Chunk 6/26 -->


Extensive benchmarks such as LongMemEval assess five fundamental long-term memory capabilities:
information extraction, temporal reasoning, multi-session reasoning, knowledge updates, and abstention
through 500 carefully selected questions, demonstrating 30% accuracy degradation in commercial assistants
throughout prolonged interactions, while automated memory evaluation frameworks facilitate thorough
assessment extending beyond passkey search methodologies [1180]. Dedicated frameworks target episodic
memory via benchmarks assessing temporally-situated experiences, with research demonstrating that cuttingedge models including GPT-4, Claude variants, and Llama 3.1 encounter difficulties with episodic memory
challenges involving interconnected events or intricate spatio-temporal associations even in comparatively
brief contexts [463]. Contemporary LLM benchmarks predominantly concentrate on assessing models’
retention of factual information and semantic relationships while substantially overlooking episodic memory
assessment—the capacity to contextualize memories with temporal and spatial occurrence details [847].


Task-specific evaluations encompass long-context passage retrieval (locating specific paragraphs within
extended contexts), long-context summarization (developing comprehensive understanding for concise
summaries), NarrativeQA (answering questions based on lengthy narratives), and specialized benchmarks
like MADail-Bench evaluating both passive and proactive memory recall in conversational contexts with
novel dimensions including memory injection, emotional support proficiency, and intimacy assessment

[1339, 1390, 556, 390]. Additional task-specific frameworks include QMSum for meeting summarization,
QuALITY for reading comprehension, DialSim for dialogue-based QA requiring spatiotemporal memory,
and MEMENTO for personalized embodied agent evaluation using two-stage processes to assess memory
utilization in physical environment tasks [1390, 572].


**Current Limitations and Challenges** Memory evaluation faces substantial challenges limiting effective
assessment of capabilities. Fundamental limitations include absence of consistent, rigorous methodologies
for assessing memory performance, particularly regarding generalization beyond training data [288]. The
lack of standardized benchmarks specifically designed for long-term memory evaluation represents another
significant obstacle, with existing frameworks often failing to capture the full spectrum of memory capabilities
needed for human-like intelligence [1079].


Architectural constraints significantly complicate evaluation efforts, as most contemporary LLM-based
agents operate in fundamentally stateless manners, treating interactions independently without truly accumulating knowledge incrementally over time [1365, 1364], despite advances in working memory through
attentional tagging mechanisms enabling flexible memory representation control [870]. This limitation prevents genuine lifelong learning assessment—a cornerstone of human-level intelligence involving continuous
knowledge acquisition, retention, and reuse across diverse contexts and extended time horizons.


36


Methodological issues arise when isolating memory-specific performance from other intelligence aspects,
challenging determination of whether failures stem from inadequate memory mechanisms or reasoning limitations [288]. Dynamic memory usage in real-world applications poses evaluation challenges, as controlled
laboratory tests inadequately capture memory system performance in complex scenarios where information
relevance changes unpredictably [1079].


**Optimization Strategies and Future Research Directions** Memory optimization encompasses diverse
techniques enhancing utilization while minimizing computational overhead and maximizing efficiency.
Biologically-inspired forgetting mechanisms provide effective optimization approaches, with frameworks like
MemoryBank implementing Ebbinghaus forgetting curves to selectively preserve and discard information
based on temporal factors and significance [1372]. Reflection-based optimization through systems like
Reflexion enables performance assessment through integrated evaluation and self-reflection, creating dual
feedback systems refining memory and behavior through continuous learning [304].


Hierarchical memory structures optimize information organization through multi-level formats enabling
efficient retrieval, demonstrated by Experience-based Hierarchical Control frameworks with rapid memory
access modules [868], memory consolidation processes through bidirectional fast-slow variable interactions

[63], and Adaptive Cross-Attention Networks dynamically ranking memories based on query relevance [410].


Future research directions encompass hybrid memory frameworks combining parametric precision
with non-parametric efficiency [942], automated feedback mechanisms for scalable response evaluation

[893], multi-agent memory systems enabling collaborative learning through shared external memories

[306], enhanced metadata learning with knowledge graph integration [896, 386], domain-specific memory
architectures for specialized applications [507], cognitive-inspired optimization incorporating memory
consolidation during inactive periods [758], and parameter-efficient memory updates through techniques
like Low-Rank Adaptation for efficient knowledge integration [428, 256]. These developments promise
advancing memory-enhanced LLM agents toward sophisticated, human-like cognitive capabilities while
addressing computational and architectural limitations, with applications extending to long-term robotic
planning, real-world decision-making systems, and collaborative AI assistants through streaming learning
scenarios and continuous feedback integration [1159, 1346, 1278].


**5.3. Tool-Integrated Reasoning**


Tool-Integrated Reasoning transforms language models from passive text generators into active world
interactors capable of dynamic tool utilization and environmental manipulation. This implementation
enables models to transcend their inherent limitations through function calling mechanisms, integrated
reasoning frameworks, and sophisticated environment interaction capabilities.


_**5.3.1. Function Calling Mechanisms**_


Function calling transforms LLMs from generative models into interactive agents through structured output
generation leveraging functions’ abstraction mechanism, enabling external tool manipulation and access to
current, domain-specific information for complex problem-solving [5, 669, 335, 882, 58, 523, 1113].


Evolution began with Toolformer’s self-supervised approach demonstrating autonomous API learning,
inspiring ReAct’s “thought-action-observation” cycle, progressing through specialized models like Gorilla
and comprehensive frameworks including ToolLLM, RestGPT, with OpenAI’s JSON standardization, while


37


**Figure** 6: Tool-Augmented Systems Framework: Evolution from text generators to world interactors through
function calling mechanisms, tool-integrated reasoning, and environment interaction capabilities.


advanced systems like Chameleon enabled multimodal question answering and TaskMatrix.AI managed AI
models across domains [939, 252, 654, 547, 923, 874, 875, 715, 659, 953].


Technical implementation involves fine-tuning (dominant method providing stable capabilities via extensive API training but requiring significant resources) and prompt engineering (flexible, resource-efficient but
unstable), with approaches like “Reverse Chain” enabling API operation via prompts, addressing challenges
in large tool management [392, 5, 1332, 791, 144, 254].


Core process encompasses intent recognition, function selection, parameter-value-pair mapping, function
execution, and response generation, with modern implementations utilizing structured LLM outputs for
external program interaction, while tools include diverse interfaces (digital systems, scratch pads, user interactions, other LLMs, developer code), requiring complex navigation of tool selection, argument formulation,
and result parsing [1268, 669, 1141, 193, 960, 590, 910].


**Training Methodologies and Data Systems** Training methodologies evolved from basic prompt-based
approaches to sophisticated multi-task learning frameworks, with fine-tuning on specialized datasets through
systems like ToolLLM and Granite-20B-FunctionCalling, beginning with synthetic single-tool data followed
by human annotations [392, 5, 357, 777, 1235].


Data generation strategies include Weaver’s GPT-4-based environment synthesis, APIGen’s hierarchical
verification pipelines (format checking, function execution, semantic verification), generating 60,000+
high-quality entries across thousands of APIs [1113, 1186, 1268, 1165, 65, 1403, 749].


Tool selection enhancement involves irrelevance-aware data augmentation, with Hammer’s function
masking techniques, oracle tool mixing for increased difficulty, tool intent detection synthesis for overtriggering mitigation, emphasizing high-quality data through stringent filtering and format verification

[670, 10, 357, 473, 1300, 218].


Self-improvement paradigms reduce external supervision dependence through JOSH algorithm’s sparse
reward simulation environments and TTPA’s token-level optimization with error-oriented scoring, demonstrating improvements while preserving general capabilities [579, 446, 366, 1271].


Sophisticated benchmarks include API-Bank (73 APIs, 314 dialogues), StableToolBench (API instability
solutions), NesTools (nested tool evaluation), ToolHop (995 queries, 3,912 tools), addressing single-tool to


38


multi-hop scenarios [621, 363, 377, 1264, 827, 995, 1257, 987].


_**5.3.2. Tool-Integrated Reasoning**_


Tool-Integrated Reasoning (TIR) represents a paradigmatic advancement in Large Language Model capabilities, addressing fundamental limitations including outdated knowledge, calculation inaccuracy, and shallow
reasoning by enabling dynamic interaction with external resources during the reasoning process [864].
Unlike traditional reasoning approaches that rely exclusively on internal model knowledge, TIR establishes a
synergistic relationship where reasoning guides complex problem decomposition into manageable subtasks
while specialized tools ensure accurate execution of each computational step [777]. This paradigm extends
beyond conventional text-based reasoning by requiring models to autonomously select appropriate tools,
interpret intermediate outputs, and adaptively refine their approach based on real-time feedback [864].


The evolution of TIR methodologies encompasses three primary implementation categories addressing
distinct aspects of tool utilization optimization. Prompting-based methods guide models through carefully
crafted instructions without additional training, exemplified by approaches that decompose mathematical
problems into executable code while delegating computation to Python interpreters [155, 601]. Supervised
fine-tuning approaches teach tool usage through imitation learning, with systems like ToRA focusing on
mathematical problem-solving by integrating natural language reasoning with computational libraries and
symbolic solvers [345]. Reinforcement learning methods optimize tool-use behavior through outcome-driven
rewards, though current implementations often prioritize final correctness without considering efficiency,
potentially leading to cognitive offloading phenomena where models over-rely on external tools [227].


In operational terms, TIR-based agents serve as intelligent orchestrators that systematically interweave
cognitive processing with external resource engagement to achieve targeted outcomes [1095]. This mechanism requires the harmonious integration of intrinsic reasoning capabilities and extrinsic tool utilization
for progressive knowledge synthesis toward objective fulfillment, where the agent’s execution pathway is
formally characterized as a structured sequence of tool activations coupled with corresponding information
assimilation events [1095]. Emerging developments have established Agentic Reasoning architectures that
amplify language model intelligence by incorporating autonomous tool-deploying agents, fluidly orchestrating web-based information retrieval, computational processing, and layered reasoning-memory integration to
tackle sophisticated challenges necessitating comprehensive research and cascaded logical analysis [1162].


**Implementation Frameworks and Paradigms** Single-tool frameworks established foundational principles
of tool-integrated reasoning through specialized implementations targeting specific computational domains.
Program-Aided Language Models (PAL) pioneered problem decomposition strategies by generating executable
code while delegating mathematical computations to Python interpreters [309]. ToolFormer demonstrated
that language models could learn external API usage with minimal demonstrations, incorporating calculators,
search engines, and diverse tools to enhance computational capabilities [939]. ToRA advanced mathematical
reasoning by integrating natural language processing with computational libraries and symbolic solvers, while
ReTool applied reinforcement learning to optimize code interpreter usage, demonstrating improvements in
self-correction patterns [345, 1320, 973]. Self-Edit utilizes execution results of generated code to improve
code quality for competitive programming tasks, employing a fault-aware code editor to correct errors based
on test case results [1318].


Multi-tool coordination systems address the complexity of orchestrating heterogeneous tools within
integrated reasoning architectures. ReAct pioneered the interleaving of reasoning traces with task-specific
actions, enabling models to think and act complementarily where reasoning supports plan tracking while


39


actions interface with external information sources [1254]. Chameleon introduced plug-and-play compositional reasoning by synthesizing programs combining vision models, search engines, and Python functions
with an LLM-based planner core [715]. AutoTools established automated frameworks transforming raw tool
documentation into executable functions, reducing manual engineering requirements in tool integration

[423, 960]. Chain-of-Agents (CoA) trains models to decode reasoning chains with abstract placeholders,
subsequently calling domain-specific tools to fill knowledge gaps [600, 1337].


Agent-based frameworks represent the most sophisticated evolution of TIR systems, moving beyond static
prompting approaches to create autonomous and adaptive AI systems. Unlike conventional tool-use that
follows rigid patterns, agent models learn to couple Chain-of-Thought (CoT) and Chain-of-Action (CoA)
patterns into their core behavior, resulting in stronger logical coherence and natural transitions between
reasoning and action [1338]. These systems build upon foundational agent architectures including reactive
systems that map perceptions directly to actions, deliberative systems implementing Belief-Desire-Intention
(BDI) models, and hybrid architectures combining multiple subsystems in hierarchical structures [734].


**Tool Categories**
**Method**


**Search &** **Computation &** **Knowledge Base** **APIs &** **Multimodal** **Language** **Interactive** **Domain-Specific**
**Retrieval** **Code Execution** **& QA** **External Services** **Tools** **Processing** **Environments** **Tools**


Table 7: Tool-augmented language model architectures: Comparison of multiple methods across 8 tool
categories including search, computation, knowledge bases, APIs, multimodal, language tools, interactive
environments, and domain-specific applications.


_**5.3.3. Agent-Environment Interaction**_


Reinforcement learning approaches have emerged as superior alternatives to prompting-based methods and
supervised fine-tuning for tool integration, enabling models to autonomously discover optimal tool usage
strategies through exploration and outcome-driven rewards [227]. ReTool exemplifies this advancement


40


by focusing on code interpreter optimization for mathematical reasoning, achieving 67.0% accuracy on
AIME2024 benchmarks after only 400 training steps, substantially outperforming text-based RL baselines
reaching 40.0% accuracy with extensive training [274]. This demonstrates that explicitly modeling tool use
within decision processes enhances both reasoning capabilities and training efficiency.


Search-augmented reasoning systems represent innovative integrations of information retrieval directly
into reasoning processes through specialized learning environments. The Search-R1 framework trains models
to make dynamic decisions about when to search and what queries to generate during multi-step reasoning
tasks, unlike traditional retrieval-augmented generation systems [984]. The architecture employs specialized
token systems structuring reasoning and search processes, where models learn to generate reasoning steps
interspersed with explicit search actions triggered through tokens that encapsulate generated queries [654].


Multi-turn and customizable tool invocation frameworks address the complexity of coordinating multiple
heterogeneous tools during reasoning processes. Recent developments include frameworks like VisTA that
use reinforcement learning to enable visual agents to dynamically explore, select, and combine tools from
diverse libraries based on empirical performance [460]. ReVeal demonstrates self-evolving code agents via
iterative generation-verification processes [512]. In multimodal domains, systems like VideoAgent employ
vision-language foundation models as tools for translating and retrieving visual information, achieving
impressive performance on video understanding benchmarks [1117, 258].


**Evaluation and Applications** Comprehensive evaluation of tool-integrated reasoning systems requires
specialized benchmarks that measure tool-integrated capabilities rather than general model performance.
MCP-RADAR provides a standardized evaluation framework employing strictly objective metrics derived
from quantifiable performance data, with extensible design spanning software engineering, mathematical
reasoning, and general problem-solving domains [314]. The framework visualizes performance through
radar charts highlighting model strengths and weaknesses across multiple dimensions, enabling systematic
comparison of tool-integrated language models regardless of implementation mechanisms.


Real-world evaluation approaches reveal significant performance gaps between current systems and
human-level capabilities, providing crucial insights into practical limitations and optimization opportunities.
The General Tool Agents (GTA) benchmark addresses limitations in existing evaluations by featuring real
human-written queries with implicit tool-use requirements, evaluation platforms with deployed tools across
perception, operation, logic, and creativity categories, and authentic multimodal inputs including images and
code snippets [1098]. Results demonstrate substantial challenges for current LLMs, with GPT-4 completing
less than 50


Function calling enabled sophisticated multi-agent systems where multiple LLM agents collaborate through
coordinated tool use and task decomposition, with MAS leveraging collective intelligence through parallel
processing, information sharing, and adaptive role assignment, while LLM integration enhanced capabilities
in planning, specialization, and task decomposition through frameworks like DyLAN, MAD, and MetaGPT

[243, 911, 348, 140, 631]. Advanced multi-agent function calling employs sophisticated orchestration
mechanisms decomposing complex tasks into manageable subtasks, with fundamental approaches involving
splitting reward machines into parallel execution units, each agent maintaining individual reward machines,
local state spaces, and propositions, while adaptive orchestration enables dynamic agent selection based on
context, responses, and status reports [39, 1056, 697, 117].


41


**5.4. Multi-Agent Systems**


Multi-Agent Systems represent the pinnacle of collaborative intelligence, enabling multiple autonomous
agents to coordinate and communicate for solving complex problems beyond individual agent capabilities.
This implementation focuses on sophisticated communication protocols, orchestration mechanisms, and
coordination strategies that enable seamless collaboration across diverse agent architectures.





**Figure** 7: Multi-Agent Systems Framework: Overview of communication protocols, orchestration mechanisms,
and coordination strategies for collaborative AI agent systems.


_**5.4.1. Communication Protocols**_


Agent communication systems originate from the Knowledge Sharing Effort of the early 1990s, establishing
foundational principles for autonomous entity coordination through standardized languages addressing
interoperability challenges [373, 93]. KQML emerged as the pioneering Agent Communication Language,
introducing multi-layered architecture separating content, message, and communication layers while employing speech act theory [373, 82, 663, 284]. FIPA ACL enhanced this foundation through semantic frameworks
based on modal logic, feasibility preconditions, and rational effects [1155, 373, 82].


Interoperability requirements necessitate semantic-level communication capabilities enabling crossplatform agent understanding without extensive pre-communication setup, addressing increasing heterogeneity through ontology-based protocol formalization and Semantic Web technologies, while incorporating
security mechanisms against communication vulnerabilities [486, 66, 449, 487, 792, 1063].


**Contemporary Protocol Ecosystem** Contemporary standardized protocols address fragmentation challenges hindering LLM agent collaboration [1244, 1137, 412]. MCP functions as “USB-C for AI,” standardizing
agent-environment interactions through JSON-RPC client-server interfaces, enabling hundreds of servers
across diverse domains while introducing security vulnerabilities [934, 250, 622, 270, 15, 261, 930, 1102,
374, 1194, 301, 1016, 719, 273].


A2A standardizes peer-to-peer communication through capability-based Agent Cards enabling task
delegation and secure collaboration via JSON-based lifecycle models [622, 250, 934]. ACP provides generalpurpose RESTful HTTP communication supporting multipart messages and synchronous/asynchronous
interactions with discovery, delegation, and orchestration features [281, 250].


ANP extends interoperability to open internet through W3C decentralized identifiers and JSON-LD graphs,
with emerging protocols AGNTCY and Agora diversifying standardization ecosystems [250, 685, 1137].


42


Progressive layering strategy: MCP provides tool access, ACP enables message exchange, A2A supports peer
interaction, ANP extends network interoperability [1015, 934].


**LLM-Enhanced Communication Frameworks** LLMs transform agent communication through sophisticated
natural language processing enabling unprecedented context sensitivity across academic and industrial
applications spanning social science, natural science, and engineering domains [492, 690, 504, 1099, 1179,
1136, 904, 1060, 879]. Enhanced systems demonstrate cognitive synergy through specialized knowledge
bases, planning, memory, and introspection capabilities, supporting cooperative, debate-oriented, and
competitive communication paradigms [492, 360].


Communication structures encompass layered hierarchical organization, decentralized peer-to-peer
networks, centralized coordination, and shared message pool architectures, complemented by sequential
exchanges, universal language interfaces, and message-passing strategies [360, 1249, 1219, 171, 400, 491,
543, 665, 799, 949].


Framework implementations support comprehensive ecosystems: AutoGen enables dynamic response
generation, MetaGPT provides shared message pools, CAMEL offers integrated orchestration, CrewAI
facilitates adaptation, with reinforcement learning integration enhancing reward redesign, action selection,
and policy interpretation [188, 38, 119, 1004, 228, 871, 935, 958, 1273]. Human-agent communication
introduces complex interaction landscapes through flexible participation and cognitive diversity, with agents
inferring communicator properties and mirroring human communicative intentions [1409, 34, 675].


_**5.4.2. Orchestration Mechanisms**_


Orchestration mechanisms constitute the critical coordination infrastructure for multi-agent systems, managing agent selection, context distribution, and interaction flow control [902], enabling effective cooperation
among human and non-human actors through user input processing, contextual distribution, and optimal
agent selection based on capability assessment and response evaluation [53], while managing message flow,
ensuring task progression, and addressing task deviations [175]. Advanced orchestration frameworks incorporate intent recognition, contextual memory maintenance, and task dispatching components for intelligent
coordination across domain-specific agents, with the Swarm Agent framework utilizing real-time outputs
to direct tool invocations while addressing limitations in static tool registries and bespoke communication
frameworks [814, 267, 250].


Contemporary orchestration strategies exhibit distinct operational paradigms: a priori orchestration
determines agent selection through pre-execution analysis of user input and agent capabilities, while
posterior orchestration distributes inputs to multiple agents simultaneously, utilizing confidence metrics
and response quality assessment as demonstrated by the 3S orchestrator framework [901]; function-based
orchestration emphasizes agent selection from available pools, contextual information management, and
conversation flow control [54]; component-based orchestration employs dynamic planning processes where
orchestrators arrange components in logical sequences based on user instructions, utilizing LLMs as component
orchestration tools to generate workflows with embedded orchestration logic [681].


Emergent orchestration paradigms include puppeteer-style orchestration featuring centralized orchestrators that dynamically direct agents in response to evolving task states through reinforcement learning-based
adaptive sequencing and prioritization, and serialized orchestration addressing collaboration topology complexity by unfolding collaboration graphs into reasoning sequences guided by topological traversal, enabling
orchestrators to select single agents at each step based on global system state and task specifications [198].


43


**Context Management and Environmental Adaptation** Context serves as the foundational element guiding
agent actions and interactions within orchestrated systems, supporting operational mode diversity while
maintaining application individuality and task execution sequencing through global state maintenance that
enables orchestration systems to track task execution progress across distributed nodes, providing agents
with contextual awareness necessary for effective subtask performance within broader workflow contexts

[26]. Session-based context refinement defines collaborative scope boundaries, facilitating event-driven
orchestration where agents can enter and exit dynamically, create output streams, and contribute to shared
session streams, with configurable sessions enabling agent inclusion based on user input or autonomous
decision-making to create adaptable systems responsive to changing task requirements [519].


Well-designed interaction structures and task orchestration mechanisms underscore context’s critical role
in scalable multi-agent collaboration. Systems adapt communication patterns and agent roles to contextual
requirements, supporting dynamic collaboration tailored to specific task demands through complex task
decomposition and suitable agent assignment for subtask execution [1137]. This contextual adaptation
encompasses both organizational and operational dimensions, enabling systems to maintain coherence while
accommodating environmental variability and evolving user requirements.


_**5.4.3. Coordination Strategies**_


Multi-agent orchestration encounters significant challenges in maintaining transactional integrity across
complex workflows, with contemporary frameworks including LangGraph, AutoGen, and CAMEL demonstrating insufficient transaction support: LangGraph provides basic state management while lacking atomicity
guarantees and systematic compensation mechanisms, AutoGen prioritizes flexible agent interactions without
adequate compensatory action management potentially resulting in inconsistent system states following partial failures, and validation limitations emerge as many frameworks rely exclusively on large language models’
inherent self-validation capabilities without implementing independent validation procedures, exposing
systems to reasoning errors, hallucinations, and inter-agent inconsistencies [128].


Context handling failures compound these challenges as agents struggle with long-term context maintenance encompassing both episodic and semantic information [214, 1122], while central orchestrator
topologies introduce non-deterministic, runtime-dependent execution paths that enhance adaptability while
complicating anomaly detection, requiring dynamic graph reconstruction rather than simple path matching

[394], and environmental misconfigurations and LLM hallucinations can distract agentic systems, with poor
recovery leading to goal deviation that becomes amplified in multi-agent setups with distributed subtasks

[214, 1099].


Inter-agent dependency opacity presents additional concerns as agents may operate on inconsistent
assumptions or conflicting data without explicit constraints or validation layers, necessitating anomaly
detection incorporating reasoning over orchestration intent and planning coherence [394], while addressing
these challenges requires comprehensive solutions such as the SagaLLM framework providing transaction
support, independent validation procedures, and robust context preservation mechanisms [128], and
approaches like CodeAct integrating Python interpreters with LLM agents to enable code action execution
and dynamic revision capabilities through multi-turn interactions [1122].


**Applications and Performance Implications** Agent and context orchestration demonstrates practical
utility across diverse application domains: healthcare applications employ context-switching mechanisms
within specialized agent-based architectures performing information retrieval, question answering, and
decision support, utilizing supervisory agents to interpret input features and assign subtasks to specialized


44


agents based on clinical query type, user background, and data modality requirements [619, 760, 1059];
network management applications leverage context-aware orchestration to address complexity challenges by
equipping Points of Access with agents dedicated to unique contexts, enabling efficient network dynamics
management through context-specific action sets including available service instances and network paths

[966].


Business process management and simulation represent significant application areas through platforms
like AgentSimulator, enabling process behavior discovery and simulation in orchestrated and autonomous
settings where orchestrated behavior follows global control-flow patterns with activity selection dependent
on previous activities and agent assignment based on capabilities and availability, while autonomous behavior
operates through local control-flow and handover patterns acknowledging agent autonomy in collaborative
work [549].


Performance implications indicate that well-designed orchestration improves system effectiveness by
leveraging distinct agent capabilities, with research demonstrating that human users frequently struggle with
effective agent selection from available sets while automated orchestration enhances overall performance

[72], motivating frameworks that learn agent capabilities online and orchestrate multiple agents under
real-world constraints including cost, capability requirements, and operational limitations, with autonomy
levels varying across implementations where some systems exhibit pronounced autonomy within designated
phases, demonstrating adaptability in action management corresponding to task specificity and reaching
Level 2 autonomy through contextual resource utilization [466].

##### **6. Evaluation**

