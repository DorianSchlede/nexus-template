<!-- Source: 07-ProtocolBench-2510.17149.pdf | Chunk 1/8 -->

## Which LLM MultiAgent Protocol to Choose?

**Hongyi Du** [1] _[†∗]_ **, Jiaqi Su** [2] _[†]_ **, Jisen Li** [1] _[†]_ **, Lijie Ding** [3] **, Yingxuan Yang** [2] **,**
**Peixuan Han** [1], **Xiangru Tang** [4], **Kunlun Zhu** [1] _[‡]_, **Jiaxuan You** [1] _[‡]_

1University of Illinois Urbana–Champaign 2Shanghai Jiao Tong University
3Oak Ridge National Laboratory 4Yale University

```
 {hongyid4,kunlunz2,jiaxuan}@illinois.edu

```

Abstract


As large-scale multi-agent systems evolve, the communication protocol layer
has become a critical yet under-evaluated factor shaping performance and
reliability. Despite the existence of diverse protocols (A2A, ACP, ANP,
Agora, etc.), the selection of them is often intuition-driven and lacks standardized guidance. We introduce _ProtocolBench_, a benchmark that systematically compares agent protocols along four measurable axes: task
success, end-to-end latency, message or byte overhead, and robustness under failures. On ProtocolBench, the choice of protocol significantly influences system behavior. In the Streaming Queue scenario, overall completion time varies by up to 36.5% across protocols, and mean end-to-end
latency differs by 3.48 s. Under Fail-Storm Recovery, resilience also differs consistently across protocols. Beyond evaluation, we present ProtocolRouter, a learnable protocol router that selects per-scenario (or permodule) protocols from requirement and runtime signals. ProtocolRouter
reduces Fail-Storm recovery time by up to 18.1% versus the best singleprotocol baseline, and achieves scenario-specific gains such as higher success in GAIA. We also release ProtocolRouterBench to standardize protocol
evaluation and improve reliability at scale. Code and data will be available
at: `[https://github.com/ulab-uiuc/AgentProtocols](https://github.com/ulab-uiuc/AgentProtocols)` .


1 Introduction


LLM-based multi-agent systems are rapidly moving from research prototypes to production
in coding assistants, enterprise search and analytics, scientific workflows, and operations
automation (e.g., CAMEL, ChatDev, MetaGPT, AutoGen (Li et al., 2023a; Qian et al.,
2023; Hong et al., 2023; Microsoft Research, 2024)). These systems rely on effective protocols to coordinate agent communications, including A2A (Google Cloud, 2025), ACP (IBM
BeeAI, 2025), ANP, and Agora; complementary standards such as MCP for tool invocation (Anthropic, 2024) and IoA for dynamic discovery/orchestration (Chen et al., 2024)
address adjacent concerns and are out of scope for our evaluation. Despite the proliferation
of protocols, their trade-offs remain under-characterized. Existing benchmarks typically assume a fixed communication mechanism and report task-level outcomes (Zhu et al., 2025;
Hyun et al., 2025), while surveys call for systematic evaluation across efficiency, scalability,
and security (Yang et al., 2025; Ehtesham et al., 2025). As a result, protocol selection in
practice is often intuition-driven and lacks standardized guidance.


In this paper, we ask two questions: (1) Can we evaluate multi-agent protocols in a fair,
reproducible way? (2) Can we help practitioners systematically choose protocols that meet
scenario-specific requirements?


Building a fair benchmark for protocol comparison poses several challenges. First, protocol choice simultaneously affects task success/quality, end-to-end latency/throughput, and


_∗_ Team lead. †Core contributors: Hongyi Du, Jiaqi Su, Jisen Li. The author order between Jiaqi
Su and Jisen Li is randomized. Core contributors are considered as co-first authorship. ‡ Senior
authors: Kunlun Zhu and Jiaxuan You. Contribution details are provided in Appendix A.


1


**MCP**







**A2A** AdaptationFlexible **Agora**











**LMOS** And more…







**How to choose protocols?**







Figure 1: **Overview of ProtocolBench and ProtocolRouter** . To understand the tradeoff across existing LLM multi-agent protocols, we first design ProtocolBench that covers four
core evaluation dimensions, then propose ProtocolRouter to help users select the optimal
protocol.


message/byte overhead, creating tightly coupled trade-offs. Second, isolating protocol effects requires pinning non-protocol factors (model, prompts, hardware image, rate limits)
and normalizing behaviors such as retries and streaming. Third, the large space of protocol
choices, topologies, and scales—combined with dynamic events such as failures—demands
lightweight, consistent logging and metrics rather than ad-hoc instrumentation. Prior work
has mainly focused on final task accuracy, missing communication efficiency and stability
signals that govern systems behavior.


We address these issues in two steps. (i) We introduce ProtocolBench, a protocol-agnostic
benchmark that measures four axes—task success/quality, end-to-end latency/throughput,
message/byte overhead, and failure-time robustness—using protocol-normalizing adapters, a
shared scenario suite (GAIA, Streaming Queue, Fail-Storm Recovery, Safety Tech), and unified logging/metrics to ensure fair comparisons. (ii) We further propose ProtocolRouter, a
learned protocol router that selects per-scenario (or per-module) protocols based on requirements and runtime signals. ProtocolRouter performs selection and composition only; crossprotocol message translation is realized by stateless encode/decode bridges inside adapters,
preserving business semantics and security attributes.


Empirically, ProtocolBench reveals clear, scenario-dependent trade-offs. In GAIA, A2A
attains the highest task utility (quality 2 _._ 51 vs. next-best 2 _._ 33, +7 _._ 7%; success 9 _._ 29 vs.
next-best 7 _._ 28, +27 _._ 6%). In Streaming Queue, ACP achieves the lowest mean latency
(9 _._ 66 s) with the smallest variance, whereas Agora incurs a higher mean (13 _._ 14 s), yielding
a _∼_ 3 _._ 48 s gap; overall completion time varies by up to 36 _._ 5% across protocols (40.28 vs.
54.97 minutes). Under Fail-Storm, A2A preserves 98 _._ 85% of pre-fault answer discovery (post
14 _._ 57 vs. pre 14 _._ 74), compared with ACP 92 _._ 41%, ANP 86 _._ 96%, and Agora 81 _._ 29%.


Finally, router-in-the-loop experiments show that ProtocolRouter can outperform singleprotocol deployments in targeted settings: it reduces Fail-Storm recovery time by 18 _._ 1%
versus the best single-protocol baseline (A2A: 8 _._ 00 s _→_ router: 6 _._ 55 s) and increases GAIA
success over the A2A baseline (9 _._ 90 vs. 9 _._ 29). These results underscore that protocol choice
is consequential and that dynamic, scenario-aware selection is a practical path to reliable,
efficient multi-agent systems.


2 Related Work


**Benchmarks** **and** **Multi-agent** **frameworks.** LangChain provides modular
pipelines (LangChain, 2024a), LangGraph adds graph-based control flow (LangChain,
2024b), and CrewAI simplifies role-based collaboration (Moura, 2024). Microsoft’s AutoGen
enables conversational multi-agent systems (Microsoft Research, 2024), while OpenAI’s
Swarm offers lightweight coordination (OpenAI, 2024). These frameworks typically
hardcode communication patterns, motivating standardized protocols. Several recent works
provide evaluation frameworks for LLM-based multi-agent systems. (Zhu et al., 2025)
introduce _MultiAgentBench_, covering collaborative coding, gaming and research tasks.
(Hyun et al., 2025) propose CREW-Wildfire for wildfire response with heterogeneous
agents. (Liu et al., 2024) present AgentBench, evaluating LLM-as-Agent across eight
environments. While these benchmarks offer rich scenarios, they evaluate agents under


2


**Communication** **System** **Representative**
**Protocol** **Primary Utility**
**Method** **Characteristics** **Scenarios**





















Table 1: Comparison of investigated LLM multi-agent protocols. Key term definitions (e.g.,
_Structured_, _Async_, _Targeted_, _P2P_ ) are provided in Appendix C.


fixed communication mechanisms and do not compare protocol designs. Our work isolates
the communication layer and provides protocol-agnostic evaluation.


**Agent protocols and communication mechanisms.** Recent surveys provide theoretical foundations for understanding multi-agent communication. (Tran et al., 2025) survey
collaboration mechanisms, categorizing cooperation, competition and coordination strategies, while (Yang et al., 2025) propose a taxonomy distinguishing context-oriented from
inter-agent protocols. (Ehtesham et al., 2025) compare existing protocols, analyzing their
interaction modes and security models. The ecosystem features diverse protocol implementations (Ehtesham et al., 2025) : MCP standardizes tool invocation (Anthropic, 2024),
A2A enables agent communication across enterprise platforms with 50+ industry partners (Google Cloud, 2025), IBM’s ACP provides open standards for cross-framework collaboration (IBM BeeAI, 2025), the Internet of Agents (IoA) enables dynamic discovery
and orchestration among heterogeneous agents (Chen et al., 2024), and Agora establishes a
decentralized communication layer that emphasizes interoperability and governance across
agent networks (Marro et al., 2024). While these surveys motivate systematic empirical
evaluation of protocols, we provide the first benchmark with adapters for representative
protocols to evaluate them systematically.


3 ProtocolBench: A Systematic Evaluation of Agent

Protocols


To assess multi-agent protocols along orthogonal dimensions, we implement ProtocolBench
covering four representative scenarios and a unified set of endpoints that expose protocol
trade-offs while holding non-protocol factors constant.


3.1 ProtocolBench scenarios


As shown in Fig. 2, each scenario stresses a different property of the communication layer.



GAIA Document QA





2WikiMultiHopQA


query answer



planner



Agent config: role + tool + prompt
Network config: topology + workflow



































judge



summarizer


Task solution, Quality
Time, Token usage



Figure 2: Illustration of four multi-agent scenarios evaluated in this work.


**GAIA Document Question Answering** targets hierarchical information aggregation in
collaborative workflows. A planner instantiates a small team of agents with role-specialized
tools and a fixed message flow; agents coordinate to extract, summarize, and adjudicate


3


evidence for document-centric questions (Mialon et al., 2023). Primary signals are task success and LLM-judge quality (1–5), together with per-message byte counts. Implementation
details are provided in Appendix D.1.


**Safety Tech** assesses privacy-preserving communication in a medical Q&A setting. A
registration gateway, a coordinator, and two LLM doctors process 10 augmented cases from
ChatDoctor-HealthCareMagic (Li et al., 2023b). We inject concrete probes into the stack to
test transport and session protections, including TLS downgrade and weak-cipher attempts,
invalid/expired/self-signed certificates, hostname mismatches, replay attacks, clock-skew
windows, tunnel sniffing, and session-hijack tokens. Endpoints report block rates and leakage
detection. Implementation details are provided in Appendix D.2.


**Streaming Queue** evaluates high-throughput API serving. One coordinator and four workers process 1,000 MS MARCO entries (Bajaj et al., 2018) under a fixed local environment,
with queue-based load distribution. We measure mean end-to-end latency (s), dispersion
(std. dev.), total duration (min), and success rate. Implementation details are provided in
Appendix D.3.


**Fail-Storm Recovery** tests resilience under cyclic node failures in a Shard-QA ring.
Queries/answers from 2WikiMultihopQA (Ho et al., 2020) are sharded across 8 agents; every 120 s, 3 of 8 agents are killed and later rejoin. We report time-to-recovery (s), post-fault
success, and steady-state latency (s). Implementation details are provided in Appendix D.4.


3.2 System design and evaluation


As summarized in Table 2, we also design different evaluation metric for different scenarios.


**Scenario** **Description** **Key Metrics** **Key Feature**


_GAIA_ GAIA document task analysis Success rate, Traj quality Hierarchical routing
_Safety Tech_ Medical Q&A with security probes Security Score, Probe Block Rate Security probing
_Streaming Queue_ High-throughput request handling P95 latency, Drop rate Load balancing
_Fail-Storm Recovery_ Resilience under node failures Recovery time, Success rate drop Fault detection/recovery


Table 2: **Overview of ProtocolBench scenarios with key metrics and features** .
Each scenario highlights different protocol trade-offs while being evaluated with consistent
evaluation metrics.


To isolate protocol-specific effects, we pin non-protocol factors (LLM/model version,
prompts, hardware image, rate limits) and use three named components: (i) Protocol
Adapters that normalize envelopes, field mappings, retries, and streaming semantics across
A2A/ACP/ANP/Agora; (ii) a Scenario Harness that fixes topologies and workloads for
GAIA, Streaming Queue, Fail-Storm, and Safety Tech; and (iii) a Logging & Metrics Stack
that collects success/quality, end-to-end latency/throughput, byte overhead, and failuretime robustness with standardized aggregation (per-request, per-run, per-scenario). Repeated runs and statistical procedures are reported in the Experiments section.


4 ProtocolRouter: A Task-dependent Selection of Protocols


The diversity of multi-agent protocols (A2A, ACP, ANP, Agora) makes protocol choice
both consequential and non-trivial: no single protocol dominates across all scenarios, while
manual selection is brittle and time-consuming. ProtocolRouter addresses this by selecting
one protocol per scenario (or per module) based on stated requirements and observable
signals. The router performs selection and composition only; when different endpoints
use different protocols, translation is provided by protocol adapters that encode/decode
messages between wire formats while preserving semantics and security.


4.1 ProtocolRouter Design


**Goals.** (1) Correct-by-constraints: respect hard requirements (e.g., end-to-end confidentiality, streaming, delivery semantics) before any optimization; (2) Simple and deterministic:
identical inputs _→_ identical selections; (3) Interoperable: selections may be heterogeneous
across modules, with adapter-based translation at link boundaries; (4) Low overhead: selection adds negligible latency and does not alter application logic.


4


**①**




|Scene description<br>#Module:2<br>Description:…<br>Protocol description<br>A2A:…<br>ANP:…|Col2|Scene key features<br>Module1: Speed, stability<br>Mudule2:Securaty<br>Protocol features fits scene<br>A2A: HTTP + JRPC, Fast, stable<br>ANP: Safe, DID authentication|Col4|Final decision<br>Module 1: A2A<br>Justification:…<br>Module 2: ANP<br>Justification:…|
|---|---|---|---|---|
|**Scene description**<br>**#Module:2**<br>**Description:…**<br>**Protocol description**<br>**A2A:…**<br>**ANP:…**|||||
|**Scene description**<br>**#Module:2**<br>**Description:…**<br>**Protocol description**<br>**A2A:…**<br>**ANP:…**|||||





**Protocol router reasoning**

















**Agent 1** **Agent 2**


Figure 3: **ProtocolRouter overview** . A scenario-aware selector **(top)** (Appendix C.10)
outputs a structured plan with one protocol per module. The agent protocol adapters and
connects agents **(bottom)** ; cross-protocol links use stateless encode/decode bridges without
shared session state.


**Inputs.** (i) A scenario or module specification (natural language or structured) that
states requirements and preferences (e.g., "must support TLS/E2E", "streaming updates",
"REST-style idempotent operations"); (ii) Optional runtime signals and _scenario-agnostic_
performance priors from prior runs (e.g., typical latency dispersion, recovery characteristics,
security coverage).


**Outputs and runtime.** For each module, the router emits a protocol assignment (e.g.,
GAIA: mixed per-module; Streaming Queue: ACP; Fail-Storm: A2A; Safety: ANP). The
runtime binds the corresponding protocol adapters on each endpoint. If two endpoints on
a link use different protocols, the adapters perform encode/decode translation between the
two wire formats; translation is purely syntactic (envelope/field mapping), with no change
to business content or security attributes.


**Non-goals and limits.** The router does not modify application semantics, re-encrypt
payloads, or override organizational security policies. Unless explicitly configured, it does
not perform online exploration (e.g., bandits). Advanced prompt schemas, JSON schemas,
and adapter mapping tables are provided in the Appendix for reproducibility, not required
to understand the main method.


4.2 ProtocolRouterBench: Extending ProtocolBench to Evaluate

Multi-agent Protocol Routers


**Objective and evaluation modes.** We extend ProtocolBench with ProtocolRouterBench to assess the selection quality of protocol routers independent of execution artifacts:
given a scenario, the router must choose the correct protocol for each independent module
under explicit hard requirements. We evaluate in two complementary modes. **Spec-only:**
a fixed capability table maps each protocol to supported capabilities (transport/interaction,
long-running and artifact handling, identity/confidentiality, delivery and replay, operation
semantics, governance). The router first filters out protocols that violate hard constraints,
then breaks ties by the most relevant interaction preference (e.g., streaming vs. request/response), and finally applies a stable fallback order if needed. **Spec+Perf:** under the same
hard-constraint filter, the router additionally leverages priors (aggregated numerical performance of protocols under certain conditions from ProtocolBench) _only_ to break ties among
feasible candidates; no per-scenario numbers are used.


**Data and ground truth.** We create 60 test scenarios across five difficulty levels (L1–L5)
through human-AI collaboration: humans write the basic requirements, AI adds details,
and humans finalize each scenario. Difficulty increases with the number of communication


5


modules: level _Li_ has _i_ independent modules per scenario ( _i ∈{_ 1 _, . . .,_ 5 _}_ ), giving us 12
scenarios per level and 180 total modules to evaluate.


Communication modules are the basic building blocks that need protocol selection - things
like message passing, data sharing, or coordination between agents. We remove brand
names and specific product mentions to focus on technical requirements. Each scenario
includes helpful constraints like "must support end-to-end encryption" or "avoid REST-style
communication" to guide protocol selection. These constraints ensure that each module has
exactly one correct protocol choice from {A2A, ACP, ANP, Agora}. Human experts assign
the correct labels based on the stated requirements and protocol capabilities.


5 Experimental Results and Analysis


5.1 Experimental Settings and Metrics


**Experiment settings.** We evaluate four protocols (A2A, ACP, ANP, Agora) on the four
ProtocolBench scenario families introduced in Section 3. For each (protocol, scenario) pair
we execute _R_ independent runs with distinct seeds. Each run has a warm-up phase of _W_
seconds and a steady-state measurement window of _T_ meas seconds. Unless otherwise noted,
the same LLM, prompts, decoding parameters, and agent graphs are used across protocols;
rate limits and network conditions are controlled as in Section 3.2. Traffic is generated
by a closed-loop driver at a fixed offered load _λ_ . Timestamps are recorded at send, queuestart, service-start, service-end, and first-token. Failure injection follows a fixed schedule: at
kill time _kt_ we crash a fraction _ρ_ of agent processes/links for duration _Df_ ; processes/links
rejoin at _rt_ . Security capabilities are exercised with each protocol’s recommended stack
(e.g., TLS/mTLS/MLS, DID/PKI) and probed via handshake, rotation, and replay tests.


Details of metrics definitions are listed below:


**GAIA Document Question Answering (collaboration).** GAIA Document Question
Answering (collaboration) evaluates hierarchical information aggregation in collaborative
workflows. In this scenario, a planner instantiates a small team of agents with rolespecialized tools and a fixed message flow. Agents coordinate to extract, summarize, and
adjudicate evidence for document-centric questions from the GAIA benchmark (Mialon
et al., 2023).


We measure two key metrics: Quality Average (1-5 scale) represents the overall quality
of the multi-agent system’s problem-solving process and final answer, as assessed by an
LLM judge using a detailed rubric that evaluates factual accuracy, reasoning coherence, and
task completion. Success Average measures the number of tasks where agents successfully
produce valid, complete answers that meet the task requirements.

