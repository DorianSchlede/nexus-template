<!-- Source: 07-ProtocolBench-2510.17149.pdf | Chunk 4/8 -->



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


The Streaming Queue scenario evaluates distributed question-answering coordination and
protocol performance in multi-agent systems. It focuses on task orchestration, load balancing across workers, and cross-protocol compatibility, covering scenario setup, intelligent task
routing, comprehensive metrics collection, and protocol-agnostic architecture design.


1. **Scenario Setup** : A centralized network comprises one coordinator and four workers,
processing 1000 preprocessed entries from the MS MARCO dataset (Bajaj et al., 2018). The
dataset is simplified to focus on communication metrics rather than task difficulty. Testing is
conducted on an AMD server localhost to eliminate network fluctuations, ensuring consistent
timing measurements.


2. **Task Processing and Load Balancing** : The coordinator employs a work-stealing
approach where workers compete for tasks from a shared queue, achieving natural load distribution based on individual worker processing speeds. The system tracks completion times,
task counts per worker, and calculates load balance variance to assess protocol communica

16


tion efficiency and stability. This approach enables evaluation of how protocol complexity,
including authentication and encryption mechanisms, affects task distribution uniformity
across workers.


3. **Metrics Collection** : Metrics focus on communication performance and stability, including: - Total test duration.

- Success rate (fraction of completed tasks).

- Response times (average, minimum, maximum, standard deviation, median).

- Load-balancing variance (task distribution across workers).

- Network errors and retries.

- Timeout counts (tasks exceeding time limits).
Network errors, retries, and timeouts are expected to be zero or consistent across protocols,
as per design.


4. **Technical Features** :

- **Load Balancing** : The coordinator uses a work-stealing approach where workers compete
for tasks, with load balance variance measured to assess distribution uniformity.

- **Local Testing** : Running on localhost isolates protocol performance from external
network variability.

- **Metric Granularity** : Per-task response times and worker-specific metrics enable
fine-grained analysis of protocol efficiency and stability.

- **Protocol Comparison** : Uniform task sets and configurations ensure fair comparisons,
with performance differences attributable to inherent protocol characteristics and implementation complexity (e.g., A2A’s lightweight routing vs. Agora’s authentication overhead).


This implementation stress-tests communication efficiency and stability, providing insights
into protocol performance under standardized workload conditions.


D.4 Fail-Storm Recovery Implementation


The Fail-Storm Recovery scenario evaluates protocol resilience under node failures in a Shard
QA setup, testing robustness, reconnect times, and collaborative performance. Below, we
detail its implementation, covering the Shard QA base scenario, failure injection, recovery
mechanisms, metrics, and technical features.


1. **Shard QA Base Scenario** : A ring topology with 8 QA agents processes groups of 8
data points from the 2WikiMultiHopQA dataset (Ho et al., 2020), including shuffled queries,
answers, and contents. Each agent receives one query and a random content segment. To
resolve the query, agents forward requests to neighbors for matching content. Messages
propagate up to 8 hops; failure occurs if unresolved after 8 hops. This tests communication
efficiency and multi-agent collaboration.


2. **Failure Injection** : Every 2 minutes during a running Shard QA session, 3 agents are
randomly terminated (killed) to simulate sudden dropouts. Killed agents initiate reconnect
attempts after a 2-second delay, mimicking realistic network recovery patterns where agents
need brief time to detect failures and initialize reconnection procedures.


3. **Recovery Mechanisms** : Upon detecting a failed target agent, messages skip it and
forward to the next in the ring. Recovery time is measured from the kill event to the
successful reconnection of the last affected agent. The process involves 3 agents departing
and rejoining, assessing network stability during transitions.


4. **Performance Phases** :

- **Pre-Fault** : The 2 minutes before a kill event, establishing baseline performance.

- **Recovery** : The period from kill to full reconnection.

- **Post-Fault** : From recovery completion to the next kill event.
Performance differences across phases (e.g., success rates, latencies) quantify robustness.


5. **Metrics Collection** : Key metrics include recovery time (seconds from fault injection
to system stabilization), answer discovery rate (percentage of queries successfully resolved,
measured pre- vs. post-fault), and steady-state average latency (task completion times
in seconds, comparing pre-fault and post-fault phases). These metrics quantify protocol


17


resilience by measuring both functional performance degradation and temporal recovery
characteristics.


6. **Technical Features** :

- **Failure Detection** : Agents detect failures via timeouts or heartbeat checks, enabling
ring skips.

- **State Recovery** : Reconnecting agents restore state from logs or peers to minimize
disruptions.

- **Fair Comparison** : Identical datasets and topologies across protocols ensure differences
stem from failure handling.

- **Simulation Controls** : Random kills are seeded for reproducibility, with multiple runs
averaging results.


This implementation rigorously assesses fault tolerance, state recovery, and sustained collaboration in dynamic multi-agent networks.


E Benchmark Implementation


**Protocol versions (frozen for reproducibility).** We pin protocol stacks to specific releases; the exact wheels and commit hashes are listed in the artifact manifest. The versions
used in all reported runs are:


**Component** **Package / Artifact** **Version**


ACP `acp-sdk` `1.0.3`
A2A `a2a-sdk` `0.3.3`
Agora `agora-protocol` `0.2.0`
ANP `agent-connect` `0.3.5`


E.1 Controls and Fairness (Details)


E.1.1 Experimental Setup: Constants and Variables


We categorize the experimental setup into pinned constants (ensuring reproducibility) and
scenario-specific variables (capturing task diversity).


**Pinned Constants.** All non-protocol factors are fixed and verified:


   - **Model and decoding:** Qwen2.5-VL-72B-Instruct; temperature=0.0, top_p=1.0,
max_tokens=4096.


   - **Hardware/OS/container:** Single-node AMD server; pinned image with identical
OS, drivers, and libraries for all runs.


   - **Prompts:** Version-anchored prompts for base system, GAIA judge, Safety evaluator, and ProtocolBench router.


   - **Rate** **limits/timeouts:** connection_timeout=10s, message_timeout=30s,
qa_cycle_timeout=15s, max_retries=3 with exponential backoff.


   - **Adapter/router versions:** Commit hashes are recorded in the artifact manifest.


   - **Internal retries/reconnects:** Disabled at protocol adapters; recovery is implemented uniformly in the upper PAL layer to avoid bias.


**Scenario Variables.** Each scenario introduces its own communication topology and dynamics:


   - **Fail-Storm (FS):** 8-node ring; at most 8 hops; skip failed nodes until recovery.


   - **Streaming Queue (SQ):** Star topology with 1 coordinator and 4 workers.


   - **GAIA:** Dynamic star; agent count increases with level (L1=2, L2=4, L3=8).


   - **Safety:** Point-to-point with two endpoints (two doctors).


18


E.1.2 Fairness verification


We perform _replay equality checks_ : given identical inputs, non-protocol side-effects (planner
outputs, tool calls) are identical across adapters. ProtocolBench operates with temperature
0 to ensure deterministic outputs. All equality checks and logs are included in the artifacts.


E.2 Windowing, Byte Accounting, and Aggregation


E.2.1 FS windowing and recovery metrics


For cycle _t_ with kill timestamp _kt_ and last reconnection timestamp _rt_ :


   - **Pre window:** [ _kt −_ 60s _, kt_ ).

   - **Recovery window:** [ _kt, rt_ ].

   - **Post window:** ( _rt, rt_ + 60s]; truncated if the next kill begins earlier.


Primary FS endpoints:
Time-to-Recovery (TTR) = _rt −_ _kt,_

Post-fault retention = [# successful requests in post]

# successful requests in pre _[.]_

If pre has zero successes, retention is marked _NA_ and excluded from aggregates.


E.2.2 Latency and percentiles


Latency distributions are summarized by mean, median, and percentile endpoints. For
SQ, the primary endpoint is P95 end-to-end latency per run; we report medians and BCa
bootstrap 95% CIs across runs.


E.2.3 Byte accounting


We separate:


   - `MSG_BYTES_PAYLOAD` : application payload bytes (requests + responses).

   - `MSG_BYTES_RETRY_OVERHEAD` : bytes due to retries and protocol-level overhead.


TLS handshakes and cryptographic negotiation bytes are excluded from both counters.
Counting is performed at the middleware boundary to avoid double counting. For streaming,
bytes are bucketed by message boundaries before aggregation.


E.2.4 Aggregation levels


   - **Per-request:** latency, payload bytes, overhead bytes.


   - **Per-run:** success rate, FS recovery metrics.


   - **Per-scenario/module:** ProtocolBench accuracies.


E.3 ProtocolRouterBench: Data, Rules, and Artifacts


E.3.1 DATA


**Corpus and ID conventions.** File: `ProtocolBench_scenarios.jsonl` with 60 scenarios. Scenario IDs: `RB-L{level}-{idx}`, where `level` _∈{_ 1 _, . . .,_ 5 _}_ and `idx` _∈{_ 01 _, . . .,_ 12 _}_ .
Module IDs: `RB-L{level}-{idx}-M{m}` (1-based). The artifact manifest `MANIFEST.yaml`
records file hashes and the commit for the corpus.


**Difficulty stratification and construction.** There are 12 scenarios per level (L1–L5).
Modules per scenario increase with level (L1:1, L2:2, L3:3, L4:4, L5:5), totaling 180 modules.
Construction constraints:


1. Explicit role/module descriptors per scenario.


2. _Lock/exclude_ _phrases_ prevent multi-label ground truth when needed
(e.g., “REST/idempotent/batch/archival” locks resource semantics; “avoid
resource/state-machine semantics” excludes them).


19


**Level** **# Scenarios** **Modules per Scenario** **# Modules**


L1 12 1 12
L2 12 2 24
L3 12 3 36
L4 12 4 48
L5 12 5 60


**Total** **60**       - **180**


Table 6: ProtocolBench difficulty breakdown.


**Rank** **Assignment** (ordered by module index) **#Mods** **Count** **Share (%)**


1 `[agora, acp]` 2 70 42 _._ 4
2 `[agora, agora, acp]` 3 33 20 _._ 0
3 `[agora, agora, agora, acp]` 4 25 15 _._ 2
4 `[acp]` 1 7 4 _._ 2
5 `[agora, a2a, agora, acp]` 4 6 3 _._ 6
6 `[agora, agora, agora, agora, acp]` 5 4 2 _._ 4
7 `[a2a, acp]` 2 4 2 _._ 4
8 `[agora, agora, a2a, acp]` 4 3 1 _._ 8
9 `[agora, agora, agora, agora, agora, agora, acp]` 7 3 1 _._ 8
10 `[agora, a2a, acp]` 3 3 1 _._ 8
11 `[agora, agora, agora, agora, agora, acp]` 6 1 0 _._ 6
12 `[agora, agora, agora, a2a, agora, agora, agora,` 8 1 0 _._ 6
```
    acp]
```

13 `[agora, agora, agora, agora, a2a, acp]` 6 1 0 _._ 6
14 `[agora, a2a, agora, a2a, acp]` 5 1 0 _._ 6
15 `[agora, agora, agora, a2a, acp]` 5 1 0 _._ 6
16 `[agora, agora, agora, agora, agora, agora,` 7 1 0 _._ 6
```
    agora, acp]
```

17 `[agora, a2a, a2a, acp]` 4 1 0 _._ 6


Table 7: GAIA — Router assignment patterns per run (total matches = 165, unique assignments = 17). Assignment lists map module _mi_ (index = position) to protocol in order.


3. No cross-module context sharing; each module is prompted and judged independently.


4. Single-choice ground truth in {A2A, ACP, Agora, ANP}.


E.3.2 RULES


**Feature facets and evidence mapping.** We fix a compact facet set and a lexicon that
maps scenario spans to facets:


   - **Transport/interaction:** SSE/streaming, RPC, batch.


   - **Long-running/artifacts:** job orchestration, checkpoints, artifacts.


   - **Identity/E2E:** DID, key material, end-to-end encryption.


   - **Delivery/replay:** at-least-once, idempotency, replay windows.


   - **Operation semantics:** REST, idempotent updates, state machines.


   - **Trust/governance:** audit, consent, policy hooks.


**Hard constraints** first prune incompatible candidates (e.g., strict E2E removes protocols without native E2E). The decision order in `priority_decide()` is identity/E2E


_→_ operation semantics _→_ interaction (streaming/long-job) . If candidates remain tied,
`pick_by_narrative()` selects the protocol whose defining capability anchor appears earliest
in the scenario text; stable fallback order: `[A2A, ACP, Agora, ANP]` .


20


**Prompt and function-call contract.** Router uses a fixed, version-anchored prompt
`PROTOCOL_SELECTION_PROMPT` as shown in G.10.2. Responses are emitted via a structured
function call with JSON fields:





Rationales must not contain numbers or performance claims. A linter enforces a field
whitelist and rejects numeric tokens in rationales.

