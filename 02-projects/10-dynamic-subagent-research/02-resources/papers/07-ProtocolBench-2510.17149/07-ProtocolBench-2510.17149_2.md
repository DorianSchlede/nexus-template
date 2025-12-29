<!-- Source: 07-ProtocolBench-2510.17149.pdf | Chunk 2/8 -->

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


**Fail-Storm Recovery (Discovery, Latency, Recovery).** For each fault cycle, we define
two measurement windows: Pre-fault (60 seconds before failure) and Post-fault (60 seconds after recovery). We measure **Answer Discovery Rate** as the percentage of queries
successfully resolved in each window, **Latency** as the median task completion time, and
**Recovery Time** as the duration from fault injection to system stabilization.


**Streaming Queue (Latency).** Let run _r_ contain _Nr_ requests indexed by _i_, with arrival
and completion times _t_ [arr] _i,r_ [and] _[ t]_ _i,r_ [done][. End-to-end(E2E) latency for request] _[ i]_ [ is]


_Ti,r_ [e2e] [=] _[ t]_ _i,r_ [done] _−_ _t_ [arr] _i,r_ _[.]_


Run-level duration (reported as “Duration (min)”) is


_[t]_ [done] _i,r_ _−_ min _i_ _t_ [arr] _i,r_
Duration [SQ] _r_ = [max] _[i]_ 60 _._


Per run, we summarize _{Ti,r_ [e2e] _[}]_ _i_ _[N]_ =1 _[r]_ [by median (Med), Min and Max.]

Tables report the run-average of these summaries across the _R_ runs.


6


**Safety Tech (Security capabilities).** We evaluate security capabilities using a binary
matrix indicating whether each protocol supports specific security features (TLS transport,
session hijacking protection, end-to-end encryption, tunnel sniffing resistance, and metadata
leakage prevention). We also measure probe block rates as the percentage of security attacks
successfully blocked by each protocol.


**Routerbench (routing capability).** Routers work the same way every time: the same
input always gives the same output. We first check hard rules, then use preferences to
choose between valid options. Any remaining ties are broken using a fixed order.


The main metric is **Scenario Accuracy**, which measures how often we get all module
choices right for a complete scenario. This means every module in a scenario must be
predicted correctly for it to count as correct.


We also track other metrics like how often individual modules are chosen correctly(module
accuracy), and we show confusion matrices to see which protocols get mixed up most often
(especially A2A and ACP). The complete dataset, scoring tools, and annotation guidelines
are in Appendix E.3. _Reporting note._ We intentionally omit generic task accuracy or F1


and other basic statistics; they are not differentiating for our protocol-level study and are
scenario-dependent. All tables (Table 3, Table 3a–Table 3d) use the definitions above.


5.2 Agentic Tasks Performance


A2A emerges as the superior protocol for overall task utility across the ProtocolBench
scenarios, achieving the highest average quality score of 2.51 and success rate of 9.29 (Table 3a). This performance advantage is particularly evident in the **GAIA** scenario, where
A2A’s hierarchical information aggregation capabilities and peer-to-peer coordination excel
in distributed document analysis tasks.


Compared to ACP, A2A demonstrates a substantial 10.57% improvement in quality metrics
and a remarkable 76.95% enhancement in success rate, establishing it as the most effective
protocol for heterogeneous collaborative workloads. From a stability perspective, the run-torun analysis reveals that ACP exhibits the most consistent quality performance with minimal
variance across three evaluation runs, while A2A shows greater variability in success rates,
indicating potential sensitivity to environmental conditions or workload characteristics in
complex multi-agent coordination scenarios.


5.3 Latency Performance and Tail Behavior


ACP demonstrates superior latency characteristics in the **Streaming Queue** scenario,
achieving the lowest mean response time of 9,663ms with the smallest variance of 1,077ms
and the most controlled maximum latency of 14,235ms (Table 3c). This consistent performance profile makes ACP particularly suitable for high-throughput API services where
latency-critical applications demand strict tail latency requirements and uniform load distribution among worker agents.


A2A follows closely with competitive latency performance, exhibiting only a 0.36% increase
in mean latency compared to ACP while maintaining reasonable tail behavior. In contrast,
ANP and AGORA incur significant latency penalties of 17.60% and 35.93% respectively,
accompanied by substantially higher variance and heavy-tail distributions that may impact
application predictability in high-throughput scenarios processing large-scale datasets like
MS MARCO entries.


5.4 Failure Recovery and Resilience


Under the **Fail-Storm Recovery** scenario testing resilience under node failures, A2A exhibits exceptional performance, maintaining 98.85% of its pre-failure answer discovery capability (14.57% vs. 14.74% pre-failure rate) as shown in Table 3b. This superior retention
capability significantly outperforms other protocols in the challenging Shard QA environment where query-answer matching must continue despite systematic node failures: ACP
retains 92.41%, ANP maintains 86.96%, and AGORA preserves 81.29% of pre-failure performance.


7


**Scenario** **Protocol** **Quality avg** **Success avg**



GAIA



ACP 2.27 5.25
A2A **2.51** **9.29**
ANP 2.14 7.28
AGORA 2.33 6.27


(a) **GAIA** . Task-utility metrics (averages only).





Fail-Storm Recovery



ACP 14.76 13.64 4.38 4.19 8.05
A2A 14.74 **14.57** 4.34 4.19 **8.00**
ANP 14.88 12.94 4.34 4.18 **8.00**
AGORA **14.91** 12.12 **4.33** **4.18** **8.00**



(b) **Fail-Storm Recovery** . Pre-/post-failure answer discovery (%), steady-state latency (s), and
recovery time (s). All times include a 2.00 s restart delay; see Appendix D.4.























Streaming
Queue



ACP **40.28** **9.66** 6.88 **14.24** **1.08**
A2A 40.45 9.70 6.94 15.13 1.13
ANP 47.38 11.36 **0.24** 50.10 5.73
AGORA 54.97 13.14 0.52 28.21 5.09



(c) **Streaming Queue** . End-to-end latency statistics (duration, mean, min, max, std.).











Safety Tech



ACP _×_ ✓ ✓ _×_ ✓
A2A _×_ ✓ ✓ _×_ ✓
ANP ✓ ✓ ✓ ✓ ✓
AGORA ✓ ✓ ✓ ✓ ✓



(d) **Safety Tech** . Binary capability matrix; ✓ indicates presence and _×_ indicates absence.


Table 3: Consolidated experimental results by scenario. Four panels correspond to GAIA
Documented QA, Fail-Storm Recovery, Streaming Queue, and Safety Tech, each reported
with scenario-appropriate metrics.


Recovery time analysis reveals relatively uniform behavior across all protocols, with recovery
times clustering around 8.0 seconds when agents reconnect to the loop topology. ACP shows
a marginal 46ms additional delay, which is negligible in practical deployment scenarios
involving distributed multi-hop question answering with periodic connection losses.


5.5 Security Capability Analysis


The **Safety Tech** scenario assessment reveals a clear bifurcation between protocol families
in privacy-preserving capabilities (Table 3d). ANP and AGORA provide comprehensive
security coverage across all evaluated dimensions, including TLS transport security, session hijacking protection, end-to-end encryption, tunnel sniffing resistance, and metadata
leakage prevention—critical features for medical Q&A scenarios handling sensitive patient
information and defending against adversarial probing attempts.


In contrast, ACP and A2A offer partial security capabilities, lacking TLS transport layer
protection and tunnel sniffing resistance while maintaining session hijacking protection, endto-end encryption, and metadata leakage prevention. This security-performance trade-off
represents a critical consideration for deployment scenarios where comprehensive privacy


8


**Scenario Accuracy** **Module Accuracy**
**Split**

**Spec-only** **Spec+Perf** **Spec-only** **Spec+Perf**


Overall (60 scen / 180 mods) 0.535 **0.633** 0.712 **0.817**


L1 (12 scen / 12 mods) **0.750** 0.667 0.750 0.667
L2 (12 scen / 24 mods) 0.500 **0.583** 0.708 **0.750**
L3 (12 scen / 36 mods) **0.750** 0.750 **0.861** 0.889
L4 (12 scen / 48 mods) 0.500 **0.917** 0.771 **0.958**
L5 (12 scen / 60 mods) 0.100 **0.250** 0.540 **0.717**


Table 4: **Router selection correctness** : overall and by difficulty across spec-only and
performance-aware conditions.


guarantees are mandatory, as ANP and AGORA’s enhanced security comes at the cost of
increased latency overhead documented in the previous subsections. The binary security
matrix demonstrates that only ANP and AGORA can fully satisfy the stringent privacy
requirements of healthcare applications with synthetic identity information protection and
resistance to registration gateway attacks.


5.6 ProtocolRouterBench: Protocol Selection Evaluation


ProtocolRouterBench isolates the protocol-selection problem in ProtocolRouter: given a
scenario graph with module specifications and cross-protocol linking rules (Fig. 3), the
selector must produce a structured plan with exactly one protocol per module that satisfies
all constraints. The suite spans 60 scenarios (180 modules) organized into five difficulty
levels (L1–L5) that progressively increase ambiguity, constraint overlap, and inter-module
coupling. We evaluate using scenario accuracy (exact plan match), module accuracy (pernode correctness), and macro-F1 to surface systematic confusions (e.g., A2A _↔_ ACP) and
the robustness of rare classes (e.g., ANP, Agora). We further contrast a spec-only selector
against a performance-aware variant that augments the same specifications with scenarioagnostic performance priors for principled tie-breaking.


5.6.1 Protocol Selection Accuracy: Spec-only vs Performance-Aware


**Setup and overall results.** We evaluate ProtocolRouter under two conditions: a _spec-only_
baseline (using protocol specifications only) and a _performance-aware_ variant (spec+perf)
that is augmented with scenario-agnostic performance priors. The benchmark covers 60
scenarios (180 modules) across five difficulty levels (L1–L5). The spec-only baseline attains
53.5% scenario accuracy and 71.2% module accuracy, with errors dominated by A2A _↔_ ACP
confusions. Adding performance priors lifts accuracy to 63.3% (scenario) and 81.7% (module), i.e., +18.3% and +14.7% respectively, and improves macro-F1 from 0.721 to 0.824
while preserving perfect recall for ANP and high precision/recall for Agora.


**What the performance priors add and where they help most.** The performanceaware condition injects latency percentiles, throughput characteristics, failure-recovery metrics, and security capabilities from Section 5 as _scenario-agnostic priors_ that are used solely
for quantitative tie-breaking in ambiguous choices (without exposing per-scenario numbers
in rationales). The largest gains appear at higher difficulties: L4 scenario accuracy jumps
from 50.0% to 91.7% (+83.4%), and L5 from 10.0% to 25.0% (+150%), primarily by reducing
A2A _↔_ ACP confusions while maintaining ANP separation and Agora robustness.


9


**Router Decision**





**Case Study: Combined protocol for each module to raise performance in GAIA**


Figure 4: **Case study** : ProtocolRouter assigns protocols per module for the GAIA metrocounting task, enabling each module to run on its most suitable protocol (e.g., Agora for
upstream discovery/compute and ACP for the final commit). This per-module assignment
yields an overall accuracy that exceeds the single-protocol A2A baseline by **6.5%** .



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

