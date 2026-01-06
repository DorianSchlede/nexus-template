<!-- Source: 07-ProtocolBench-2510.17149.pdf | Chunk 3/8 -->

**GAIA (per-module selection)**


**Metric** **Router** **Best Single**


Quality avg (1–5) 2.50 **2.51 (A2A)**
Success avg **9.90** 9.29 (A2A)


**Fail-Storm (router: A2A)**


**Metric** **Router** **Best Single**


Pre-failure disc. (%) 14.86 **14.91 (Agora)**
Post-failure disc. (%) 13.98 **14.57 (A2A)**
Recovery time (s) **6.55** 8.00 (A2A)



**Streaming Queue (router: ACP)**


**Metric** **Router** **Best Single**


Duration (s) **2375** 2417 (ACP)
Mean latency (ms) **9495** 9663 (ACP)
Std. dev. (ms) 2866 **1077 (ACP)**


**Safety (secure protocol selected)**


**Security Check** **Router** **Best Single**


TLS transport ✓ ✓(ANP)
Session protection ✓ ✓(ANP)
E2E encryption ✓ ✓(ANP)
Tunnel resistance ✓ ✓(ANP)
Metadata protection ✓ ✓(ANP)



Table 5: **Router execution validation** : performance comparison against the best singleprotocol baselines across four scenario types.


5.6.2 Router performance validation on ProtocolBench


We also test our Protocol router on ProtocolBench. We use Spec-only Prompts to let router
Choose protocols. We examine both router’s ability to choose protocol(combinations) and
performace on each scenarios. We assume each agent in GAIA as a module in real network,
and assign each agent a protocol. For the rest of three, all network are seen as one module
and will assign only one protocol.


**Router deployment strategy.** For each scenario, ProtocolRouter selects protocols based
on scenario characteristics: **Streaming Queue** _→_ **ACP** (latency-optimized), **Fail-Storm**
_→_ **A2A** (resilience-focused), **GAIA** _→_ per-module dynamic selection (see the empirical
assignment distribution in Table 7, dominated by mixed bundles), and **Safety** _→_ **ANP**
(secure protocol). Except for GAIA’s special case, the selections for the other three scenarios
align with expectations.


**Performance analysis.** ProtocolRouter demonstrates competitive performance across all
scenarios while providing adaptive protocol selection (Table 5). The router achieves lower
latency in Streaming Queue, significantly reduces recovery time in Fail-Storm (6.55s vs
8.00s), yields higher success rates in GAIA (9.90 vs 9.29), and ensures perfect security
compliance in Safety scenarios.


10


6 Conclusion


This paper introduces ProtocolBench, the first comprehensive benchmark for evaluating
agent communication protocols, and ProtocolRouter, a dynamic router that leverages protocol diversity for improved performance. Our systematic evaluation across diverse scenarios reveals that protocol choice significantly impacts system behavior across multiple
dimensions—no single protocol dominates universally. By providing standardized evaluation tools and demonstrating the benefits of dynamic selection, we aim to transform protocol
choice from ad-hoc decisions to principled engineering. As multi-agent systems mature from
research curiosities to production infrastructure, understanding and optimizing communication layers becomes essential for building reliable, efficient, and scalable deployments.


7 Ethics Statement


Benchmarking communication protocols raises several ethical considerations. Efficient agent
coordination could enable both beneficial applications and harmful automation. We explicitly exclude scenarios involving deception, manipulation, or privacy violation from our
benchmark. The open-source release includes usage guidelines emphasizing responsible deployment.


Our fault injection experiments simulate infrastructure failures rather than adversarial attacks, avoiding the creation of tools for system disruption. We engage with the security
community to ensure our protocol adapters do not introduce new vulnerabilities.


Acknowledgment


L. Ding is supported by the Laboratory Directed Research and Development Program of
Oak Ridge National Laboratory, managed by UT-Battelle, LLC, for the US DOE.


=======


References


Anthropic. Model Context Protocol. `[https://modelcontextprotocol.io](https://modelcontextprotocol.io)`, 2024. Accessed:
2025.


Payal Bajaj, Daniel Campos, Nick Craswell, Li Deng, Jianfeng Gao, Xiaodong Liu, Rangan
Majumder, Andrew McNamara, Bhaskar Mitra, Tri Nguyen, Mir Rosenberg, Xia Song,
Alina Stoica, Saurabh Tiwary, and Tong Wang. Ms marco: A human generated machine
reading comprehension dataset, 2018. URL `[https://arxiv.org/abs/1611.09268](https://arxiv.org/abs/1611.09268)` .


Weize Chen, Ziming You, Ran Li, Yitong Guan, Chen Qian, Chenyang Zhao, Cheng Yang,
Ruobing Xie, Zhiyuan Liu, and Maosong Sun. Internet of agents: Weaving a web of
heterogeneous agents for collaborative intelligence, 2024. URL `[https://arxiv.org/abs/](https://arxiv.org/abs/2407.07061)`
`[2407.07061](https://arxiv.org/abs/2407.07061)` .


Abul Ehtesham, Aditi Singh, Gaurav Kumar Gupta, and Saket Kumar. A survey of agent
interoperability protocols: Model context protocol (MCP), agent communication protocol
(ACP), agent-to-agent protocol (A2A), and agent network protocol (ANP). _arXiv preprint_
_arXiv:2505.02279_, 2025. URL `[https://arxiv.org/abs/2505.02279](https://arxiv.org/abs/2505.02279)` .


11


Google Cloud. Agent2Agent Protocol (A2A). Technical report, Google, 2025. With support from 50+ technology partners including Atlassian, Box, Cohere, Intuit, MongoDB,
PayPal, Salesforce, SAP, ServiceNow.


Xanh Ho, Anh-Khoa Duong Nguyen, Saku Sugawara, and Akiko Aizawa. Constructing
a multi-hop qa dataset for comprehensive evaluation of reasoning steps. _arXiv preprint_
_arXiv:2011.01060_, 2020.


Sirui Hong, Mingchen Zhuge, Jiaqi Chen, Xiawu Zheng, Yuheng Cheng, Ceyao Zhang,
Jinlin Wang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, Liyang Zhou, Chenyu Ran,
Lingfeng Xiao, Chenglin Wu, and Jürgen Schmidhuber. Metagpt: Meta programming
for a multi-agent collaborative framework. _arXiv preprint arXiv:2308.00352_, 2023. URL
`[https://arxiv.org/abs/2308.00352](https://arxiv.org/abs/2308.00352)` .


Mengkang Hu, Yuhang Zhou, Wendong Fan, Yuzhou Nie, Bowei Xia, Tao Sun, Ziyu
Ye, Zhaoxuan Jin, Yingru Li, Qiguang Chen, Zeyu Zhang, Yifeng Wang, Qianshuo
Ye, Bernard Ghanem, Ping Luo, and Guohao Li. Owl: Optimized workforce learning
for general multi-agent assistance in real-world task automation, 2025. URL `[https:](https://arxiv.org/abs/2505.23885)`
`[//arxiv.org/abs/2505.23885](https://arxiv.org/abs/2505.23885)` .


Jonathan Hyun, Nicholas R. Waytowich, and Boyuan Chen. CREW-Wildfire: Benchmarking agentic multi-agent collaborations at scale. _arXiv preprint arXiv:2507.05178_, 2025.
URL `[https://arxiv.org/abs/2507.05178](https://arxiv.org/abs/2507.05178)` .


IBM BeeAI. Agent Communication Protocol (ACP). `[https://docs.beeai.dev/acp/](https://docs.beeai.dev/acp/alpha/introduction)`
`[alpha/introduction](https://docs.beeai.dev/acp/alpha/introduction)`, 2025. IBM Research.


LangChain. LangChain: Building applications with LLMs through composability. `[https:](https://github.com/langchain-ai/langchain)`
`[//github.com/langchain-ai/langchain](https://github.com/langchain-ai/langchain)`, 2024a. Accessed: 2025.


LangChain. LangGraph: Build resilient language agents as graphs. `[https://github.com/](https://github.com/langchain-ai/langgraph)`
`[langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)`, 2024b. Accessed: 2025.


Guohao Li, Hasan Abed Al Kader Hammoud, Hani Itani, Dmitrii Khizbullin, and Bernard
Ghanem. Camel: Communicative agents for "mind" exploration of large language model
society. _arXiv preprint arXiv:2303.17760_, 2023a. URL `[https://arxiv.org/abs/2303.](https://arxiv.org/abs/2303.17760)`
`[17760](https://arxiv.org/abs/2303.17760)` .


Yunxiang Li, Zihan Li, Kai Zhang, Ruilong Dan, Steve Jiang, and You Zhang. Chatdoctor:
A medical chat model fine-tuned on a large language model meta-ai (llama) using medical
domain knowledge. _Cureus_, 15(6), 2023b.


Xinbin Liang, Jinyu Xiang, Zhaoyang Yu, Jiayi Zhang, Sirui Hong, Sheng Fan, and Xiao
Tang. Openmanus: An open-source framework for building general ai agents, 2025. URL
`[https://doi.org/10.5281/zenodo.15186407](https://doi.org/10.5281/zenodo.15186407)` .


Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, Hangliang
Ding, Kaiwen Men, Kejuan Yang, Shudan Zhang, Xiang Deng, Aohan Zeng, Zhengxiao
Du, Chenhui Zhang, Sheng Shen, Tianjun Zhang, Yu Su, Huan Sun, Minlie Huang, Yuxiao
Dong, and Jie Tang. AgentBench: Evaluating LLMs as agents. In _ICLR_, 2024.


Samuele Marro, Emanuele La Malfa, Jesse Wright, Guohao Li, Nigel Shadbolt, Michael
Wooldridge, and Philip Torr. A scalable communication protocol for networks of large
language models, 2024. URL `[https://arxiv.org/abs/2410.11905](https://arxiv.org/abs/2410.11905)` .


Grégoire Mialon, Clémentine Fourrier, Craig Swift, Thomas Wolf, Yann LeCun, and Thomas
Scialom. Gaia: a benchmark for general ai assistants, 2023. URL `[https://arxiv.org/](https://arxiv.org/abs/2311.12983)`
`[abs/2311.12983](https://arxiv.org/abs/2311.12983)` .


Microsoft Research. AutoGen: Enable next-gen large language model applications. `[https:](https://github.com/microsoft/autogen)`
`[//github.com/microsoft/autogen](https://github.com/microsoft/autogen)`, 2024. Microsoft.


João Moura. CrewAI: Framework for orchestrating role-playing autonomous AI agents.
`[https://github.com/joaomdmoura/crewAI](https://github.com/joaomdmoura/crewAI)`, 2024. Accessed: 2025.


12


OpenAI. Swarm: Educational framework for multi-agent orchestration. `[https://github.](https://github.com/openai/swarm)`
`[com/openai/swarm](https://github.com/openai/swarm)`, 2024. OpenAI.


Chen Qian, Wei Liu, Hongzhang Liu, Nuo Chen, Yufan Dang, Jiahao Li, Cheng Yang,
Weize Chen, Yusheng Su, Xin Cong, Juyuan Xu, Dahai Li, Zhiyuan Liu, and Maosong
Sun. Chatdev: Communicative agents for software development. _arXiv preprint_
_arXiv:2307.07924_, 2023. URL `[https://arxiv.org/abs/2307.07924](https://arxiv.org/abs/2307.07924)` .


Khanh-Tung Tran, Dung Dao, Minh-Duong Nguyen, Quoc-Viet Pham, Barry O’Sullivan,
and Hoang D. Nguyen. Multi-agent collaboration mechanisms: A survey of LLMs. _arXiv_
_preprint arXiv:2501.06322_, 2025. URL `[https://arxiv.org/abs/2501.06322](https://arxiv.org/abs/2501.06322)` .


Yingxuan Yang, Huacan Chai, Yuanyi Song, Siyuan Qi, Muning Wen, Ning Li, Junwei Liao,
Haoyi Hu, Jianghao Lin, Gaowei Chang, Weiwen Liu, Ying Wen, Yong Yu, and Weinan
Zhang. A survey of AI agent protocols. _arXiv preprint arXiv:2504.16736_, 2025. URL
`[https://arxiv.org/abs/2504.16736](https://arxiv.org/abs/2504.16736)` .


Kunlun Zhu, Hongyi Du, Zhaochen Hong, Xiaocheng Yang, Shuyi Guo, Zhe Wang, Zhenhailong Wang, Cheng Qian, Xiangru Tang, Heng Ji, and Jiaxuan You. MultiAgentBench: Evaluating the collaboration and competition of LLM agents. _arXiv preprint_
_arXiv:2503.01935_, 2025. URL `[https://arxiv.org/abs/2503.01935](https://arxiv.org/abs/2503.01935)` .


A Core Author Contributions


**Randomized order note.** The author order between **Jiaqi Su** and **Jisen Li** is randomized.
Core contributors are considered as co-first authorship.


- **Hongyi Du** : Team leader. Framework design and implementation of ProtocolBench and
ProtocolRouter. Scenario design and code implementation of Fail Storm Recovery and
Streaming Queue. Protocol implementation (A2A, ACP, ANP, Agora, ProtocolRouter)
of all scenarios in ProtocolBench. Code implementation of Protocol Adapter of A2A in
ProtocolRouter. Main paper writing. Paper writing of appendix D, E and G.


- **Jiaqi Su** : Core contributor. Scenario design and implementation of GAIA. Protocol
implementation(ANP, Agora, ProtocolRouter) of all scenarios in ProtocolBench. Paper
writing of appendix D and F.


- **Jisen Li** : Core contributor. Scenario design and implementation of Safety Tech and Fail
Storm Recovery. Protocol implementation(A2A, ACP, ANP, Agora, ProtocolRouter) of
all scenarios in ProtocolBench. Paper writing of appendix D.


- **Lijie Ding** : Initial code implementation of Safety Tech. Code implementation of Protocol Adapter of ACP in ProtocolRouter. Main paper writing.


- **Yingxuan Yang** : Code implementation of Protocol Adapter of Agora in ProtocolRouter. Main paper writing.


- **Peixuan Han** : Main paper writing.


- **Xiangru Tang** : Main paper writing.


- **Kunlun Zhu** : Co leader. Initial idea suggestion. Code implementation of Protocol
Adapter of ANP in ProtocolRouter. Main paper writing.


- **Jiaxuan You** : Supervision; conceptualization and problem framing; methodology guidance; writing—review & editing.


B Limitations and Future Work


While ProtocolBench provides comprehensive protocol evaluation, several limitations merit
discussion. Our scenarios, though representative, cannot capture all possible agent communication patterns. Edge cases like byzantine failures or adversarial agents remain unexplored. The focus on LLM-based agents may not generalize to hybrid systems incorporating
traditional software components.


13


ProtocolRouter’s learning approach assumes stationary or slowly-changing workload distributions. Rapid context switches or rare events may not provide sufficient signal for adaptation. The computational overhead of maintaining multiple protocol states could become
prohibitive at very large scales.


Future work should expand scenario coverage, particularly for emerging patterns like agent
swarms and hierarchical delegation. Integration with production orchestration systems
would enable real-world validation. Theoretical analysis of protocol complexity bounds
and impossibility results would complement our empirical findings.


C Protocol Terminology and Capability Facets


**Structured (communication method).** Messages conform to an explicitly versioned
schema (envelope + fields) with validation at send/receive; schema violations fail fast.
Typical features include typed payloads, required/optional fields, and deterministic codec
mappings.


**Async (communication method).** Decoupled send/receive with queue- or event-driven
delivery; producers and consumers progress without lockstep rounds. Delivery may be atleast-once with idempotency keys for de-duplication; eventual consistency is acceptable.


**Targeted (communication method).** Unicast to a single selected agent or module (rather
than broadcast/multicast). A router picks one feasible destination per hop using constraints/policies; backpressure and retry respect that single target.


**P2P (communication method).** Peer-to-peer links without a central broker. Discovery is
overlay-based (e.g., gossip/registry); routing is hop-wise between peers. Reliability, ordering,
and identity are achieved by end hosts or overlay mechanisms.


**Long-running / job semantics.** Operations that span multiple steps/time windows and
expose status transitions ( `pending` _→_ `running` _→_ `committed` / `aborted` ); may support
progress streaming and resumable retrieval.


**Streaming (SSE/WS).** First-byte latency is favored by chunked delivery via Server-Sent
Events or WebSocket. Streams carry partial tokens/updates before a final commit or terminal state.


**Idempotency and replay window.** Each request carries an `idempotency_key` ; servers
coalesce duplicates across a bounded replay window. This enables safe retries and reduces
tail amplification under failures.


**End-to-end (E2E) confidentiality.** Payload content is encrypted from sender to intended
receiver(s) beyond transport-level TLS, typically using application-layer or identity-bound
cryptography; intermediaries cannot read plaintext content.


**Identity and trust.** Authentication/authorization primitives (e.g., enterprise PKI, DIDbased identity) bind messages and sessions to verifiable principals; support for key rotation,
revocation, and audit trails is considered part of the trust fabric.


**Governance and routine/versioning.** Protocols may expose routine manifests and versioned procedures (e.g., `protocolHash` ) to make interactions auditable and reproducible
across heterogeneous stacks.


D Detailed description of benchmark implementation


D.1 GAIA Document Question-Answering Implementation


The GAIA Document Question-Answering scenario evaluates hierarchical information aggregation in multi-agent protocols. Below, we detail its implementation, covering the planner
module, agent lifecycle, network memory, evaluation pipeline, sandboxed execution, time
accounting, adjudication, and fairness mechanisms.


1. **Planner Module** : A large language model (LLM) generates a JSON manifest encoding agent configurations (roles, toolsets, prompt templates), tool-call metadata (interfaces,
arguments, outputs), and network topology with explicit workflow and message-flow definitions. Discrete difficulty levels map to agent counts (2, 4, or 8 agents for levels 1, 2, or 3)


14


to ensure reproducibility, with a recorded prompting seed. The manifest ensures identical
configurations across protocols for fair comparisons.


2. **Agent Lifecycle and Network Communication** : Agents operate in a distributed
communication model where any agent can communicate with any other agent in the network
through unique addressable endpoints. They follow the manifest’s workflow, processing
messages by parsing inputs, invoking tools or LLMs, and routing responses to designated
next hop(s). The network layer abstracts protocol differences and ensures reliable message
delivery.


3. **Step-Based Network Memory** : An append-only memory pool logs all interactions
in structured JSON, capturing step indices, agent IDs, fine-grained timestamps, execution
status, and message histories with tool invocations. The memory supports offline analysis,
replay, and LLM-driven summarization.


4. **LLM-Based Summarization and Evaluation** : Post-workflow, an LLM summarizer
generates a concise outcome from the memory pool using a standardized prompt. A separate
LLM judge evaluates the result and execution log against a rubric assessing factual accuracy,
relevance, and completeness. The pipeline records resource metrics (e.g., token usage, time).


5. **Tool Design and Execution** : Many distinguished open-source agent collaboration
frameworks Liang et al. (2025); Hu et al. (2025) provide high-quality toolkits. Building
upon these advancements, the tools in our GAIA scenario are designed through selective
reuse and adaptation, enabling both efficient integration and tailored functionality. All
code execution tools operate within isolated environments with virtualized dependencies,
restricted filesystem/network access, and resource limits (CPU, memory, wall time). Logs
and artifacts are captured and linked to execution steps to facilitate traceability and reproducibility.


6. **Fine-Grained Time Accounting** : Timestamps are recorded at agent, step, and workflow levels in milliseconds (Unix epoch), enabling latency profiling and straggler detection.


7. **LLM-Driven Adjudication** : The LLM judge assesses outcomes using structured
prompts and rubric criteria, producing pass/fail results and quality scores (e.g., accuracy,
task alignment). Judgments are stored as structured metadata.


8. **Metrics and Reporting** : The evaluation report includes comprehensive performance
metrics (success rate, execution time breakdown, resource consumption by agent and task),
quality scores with detailed LLM judge analysis, and operational statistics (task completion
rates, communication overhead). Reports are emitted in both structured JSON format and
human-readable console summaries with visual indicators.


9. **Experimental Fairness** : All protocols use the same planner-generated manifest and
canonical seed to control variability, ensuring only protocol implementations differ.


This implementation ensures rigorous, reproducible evaluation of hierarchical routing in
multi-agent settings, with detailed metrics and fairness controls.


D.2 Safety Tech Implementation


The Safety Tech scenario evaluates privacy-preserving protocols in medical Q&A under
adversarial conditions, focusing on protocol-stack security penetration testing and multidimensional confidentiality protection.Below, we detail its implementation, including scenario setup, test points, probe mechanisms, reporting, and technical features.


1. **Scenario Setup** : The setup launches a registration gateway (RG), coordinator, and
two LLM doctors using native protocols (e.g., Agora_Doctor_A/B, ANP_Doctor_A/B).
Doctors register with the RG, pull directories via the coordinator, and engage in bidirectional communication through protocol-specific endpoints. The system processes 10 augmented cases from ChatDoctor-HealthCareMagic-100k with synthetic identity information.
Comprehensive probe mode is enabled via environment variables, injecting probes real-time
into message/HTTP/TLS paths using a unified `probe config` for protocol-agnostic testing
across Agora SDK, ANP DID encryption, ACP routing, and A2A execution.


15


2. **Transport and Certificate Security** : Conducts 3 rounds of TLS downgrade attacks
using weak cipher suites, obsolete TLS versions, and HTTP plaintext fallback, recording
success and block rates for each attempt. A comprehensive certificate matrix systematically verifies security blocking across 6 test dimensions: expired certificates, self-signed
certificates, hostname mismatches, incomplete certificate chains, weak cipher suites, and
TLS version downgrades. Each matrix test generates detailed blocking metrics and assigns
scores based on successful interception prevention, providing a systematic assessment of
transport-layer security robustness.


3. **End-to-End Payload Confidentiality** : Injects watermarks and plaintext probes (e.g.,
`PLAINTEXT_PROBE_*`, `HIDDEN_MARKER:S2_E2E_WATERMARK_TEST_*` ) into payloads. Uses
`tcpdump` on the `lo0` interface (8 seconds) to capture network traffic and detect plaintext
leakage through sensitive keyword matching. The system evaluates encryption effectiveness by analyzing watermark visibility and sensitive keyword hits (e.g., patient ID, SSN,
credit card numbers), assigning scores based on watermark injection participation and leak
prevention performance.


4. **Session and Timing Protection** : For session hijack, injects privilege-escalation tokens (e.g., `expired_session_*`, `admin_session_*` ), measuring interception rates via denials or 404s. Clock skew tests _±_ 30s/ _±_ 2m/ _±_ 5m/ _±_ 10m offsets and window anomalies (e.g.,
`TIME_SKEW`, `WINDOW_REPEAT/DISORDER/DUPLICATE` ) over 12 rounds. Replay attacks involve
2 rounds of old message replays, distinguishing real blocks from errors like ReadTimeout/500.


5. **Metadata and Side-Channel Protection** : Probes endpoints (e.g., `/health`,
`/metrics`, `/status` ) for exposed meta-info, quantifying exposure counts. `tcpdump` analyzes plaintext bytes and sensitive keyword hits to assess information leakage and calculate
metadata exposure scores.


6. **Real-Time Probe Injection Mechanism** : Probes are injected via protocol clients’
`send()` methods into native paths (e.g., before Agora SDK calls, ANP signatures, ACP
requests). The system dispatches `probe_config` parameters for clock skew, watermarks,
and replays, ensuring authentic testing.


7. **Weighting and Reporting** : Employs a multi-dimensional assessment system across
TLS/transport security, session hijack protection, E2E encryption detection, tunnel sniffing,
and metadata leakage dimensions.


8. **Technical Features** : Unified `ProbeConfig` class standardizes parameters (e.g.,
`tls_downgrade`, `e2e_payload_detection`, `time_skew_matrix` ) for cross-protocol consistency. Real-time injections in native paths ensure authenticity. Multi-dimensional assessment covers transport, application, session, and timing layers comprehensively.


This implementation provides a robust, protocol-agnostic framework for evaluating adversarial robustness and privacy protection capabilities across multi-agent communication protocols.


D.3 Streaming Queue Implementation

