<!-- Source: 07-ProtocolBench-2510.17149.pdf | Chunk 7/8 -->



- Official SDK tasks

- Single round Conversation: `POST /agora`

- Multi-round Conversation: `/conversations/conversationId`

```
{"status":"...", "body":"...}

```

G.8 Implementation Guidance and Versioning


- **Protocol** **name** **convention** : `protocol_name` is lowercase
`"a2a"|"acp"|"anp"|"agora"` and must match `ENCODE_TABLE/DECODE_TABLE` keys.

- **Version** **negotiation** : Expose `protocolVersion` in cards; optionally include
`min_version/max_version` in `context` for soft negotiation.

- **Observability and label cardinality** : Restrict metric labels to `(src_agent, dst_id,`
`protocol)` to avoid high cardinality (e.g., dynamic URLs/tenants).

- **Rollback and canarying** : Keep old codecs and switch using `meta.protocol_hint` or
advertised capabilities.

- **Production** **essentials** : Implement idempotency/dedup on the server
( `id` / `idempotency_key` ); for ANP, disable test bypasses and enforce strict DID/key
governance.


G.9 Router Layer Technical Details


This subsection replaces the previous router notes with a complete, self-contained specification. The Router sits above PAL and decides _where_ and _how_ to send a UTE-based request.
It implements destination selection, policy enforcement, resilience primitives (retry/backoff/circuit breaking/hedging), ordering semantics, and observability. It preserves PAL’s
security posture and never alters business semantics.


**Goal and scope.** Given (i) a Canonical Feature Model (protocol features) of protocol
capabilities and (ii) a natural-language scenario, the router deterministically selects _exactly_
_one_ protocol per module from { `A2A`, `ACP`, `ANP`, `AGORA` } and emits a structured decision
record. A network builder then assembles homogeneous or heterogeneous links accordingly.
When links are heterogeneous, messages are bridged through the _same_ UTE using _stateless_
encode/decode only, preserving business semantics and security attributes. By default the
router runs in a _spec-only_ regime (no historical numbers or hidden heuristics).


**Inputs, outputs, and determinism.** _Inputs:_ scenario text _S_ ; module set _M_ ; the protocol
features (boolean/enumerated facets with compatibility constraints). _Output (fixed JSON):_





The router runs with temperature = 0; identical inputs yield identical outputs. Rationales
cite only extracted evidence spans; no numeric claims or invented capabilities.


**protocol features.** Capabilities are organized into six facets: (1) transport & interaction
(sync/async, streaming, persistent session, back-pressure); (2) long-running & artifacts (run
lifecycle, status/resume, artifact refs/transfer); (3) identity & confidentiality (enterprise authN/Z, DID, E2E, mTLS); (4) delivery & replay (ordering, idempotency keys, replay/offset,
dedup); (5) operation semantics (REST/idempotent/batch/resource-oriented vs. conversational/NL routines); (6) cross-org trust & governance (interop, routine governance/versioning). Hard constraints remove incompatible protocols upfront (e.g., strict E2E excludes
protocols without confidentiality).


34


**Spec-only selection pipeline.** Three stages: evidence extraction _→_ semantic mapping
_→_ candidate reduction and priority. Fixed priority for tie-breaking: (i) identity/confidentiality _→_ (ii) operation semantics (REST/idempotent vs. conversational) _→_ (iii) interaction
preferences (streaming/long-job).



_Where to modify:_ adjust `priority_decide(...)` for a different priority order; extend the
candidate set and `is_protocol_compatible` for new protocols.


**Helper interfaces.**


- `extract_evidence_spans(text)` _→_ `List[str]` : rule/regex phrase extractor (temperature = 0).


- `map_spans_to_cfm(spans, cfm)` _→_ `Set[cap]` : phrase _→_ capability alignment.


- `is_protocol_compatible(proto, caps, cfm)` _→_ `bool` : hard-constraint check.


- `priority_decide(candidates, caps)` _→_ `str|List[str]` : fixed-priority chooser.


- `pick_by_narrative(text, candidates)` _→_ `str` : deterministic tie-break by narrative
consistency.


**Communication semantics for cross-protocol links.** We enforce " _change transport, not_
_semantics or security_ ." Homogeneous links use the chosen protocol natively. Heterogeneous
links install _stateless_ bridges around the UTE:


- **Envelope (illustrative JSON).**


35


- **Bridging** **policy** : install `encode(Envelope, proto)` and `decode(ProtoMsg)` _→_
`Envelope` per heterogeneous edge; bridges perform only field re-mapping and semantic
alignment, never altering business content or security markers.


- **Feature** **toggles** : if selections imply streaming/long-job/artifact/statesync/identity/E2E, the link activates native protocol primitives (e.g., SSE/WS,
status endpoints, DID+E2E).


- **Causality & errors** : messages carry unified `trace_id` / `parent_id` ; errors map to a
common taxonomy (timeout/HTTP/connection/codec/unsupported).


**Router base interface.**





**Policies and resilience.** Selection policies: static _first-match_ ; weighted; latency-aware
(EWMA/percentile-aware); consistent hashing by `session_id` / `trace_id` . Resilience primitives: jittered exponential backoff; hedging with cancel-on-first-success; circuit breaking (open/half-open/close); bulkheading via per-slot concurrency caps. Ordering can
be enforced with per- `trace_id` / `session_id` work queues; idempotency is preserved via
`context.idempotency_key` and an optional client-side request cache.


**Deterministic tie-break with a protocol-level prior (optional).**





**Online bandit overlay (optional).** After hard-constraint pruning, a contextual bandit
(e.g., Thompson sampling) may choose among feasible protocols using runtime feedback
while _respecting_ all security/semantic invariants.


36


**From decisions to network (complete function).**







**Security posture and observability.** Routers must not downgrade PAL security: preserve `Authorization` headers, mTLS bindings, and ANP DID constraints. Observability exports `ROUTER_DECISIONS`, `HEDGE_FIRES`, `CIRCUIT_STATE`, `QUEUE_DEPTH`, end-to-end
`REQUEST_LATENCY` ; all correlated via `trace_id` .


**Testing matrix.**


- **Policy conformance** : selection, sticky sessions, hedging, retry categories.


37


- **Failure drills** : open circuit, half-open probes, bulkhead saturation.


- **Ordering** : monotonic sequence under enforced queues.


- **Streaming** : hedged streams deduplicated; cancellation correctness.


G.10 Router Prompts


G.10.1 Fail Storm Router Prompt





38


```
- Discovery: /.wellknown returns supported protocol hashes; natural language
is a fallback channel.
- Evolution: Reusable "routines"; fast protocol evolution and heterogeneity
tolerance.
- Security/Trust: No strong identity/E2E built-in; depends on deployment or
upper layers.
- Typical Strengths: lightweight, negotiation-friendly, highly adaptable for
research/decentralized experiments, balanced recovery.
- Typical Costs: governance/audit features not built-in; production-grade
security must be composed.
- Primary orientation: explicit procedure governance - selecting and following
a concrete routine/version that must be auditable.
- Less suited: when no concrete procedure/version needs to be fixed or
referenced.

ANP (Agent Network Protocol)
- Positioning: Network & trust substrate for agents; three layers:
identity+E2E, meta-protocol, application protocols.
- Performance: avg 4.78-6.76s response, 10.0s recovery time (slowest), 61.0%
success rate (highest), 22.0% answer discovery rate (highest)
- Security/Trust: W3C DID-based identities; ECDHE-based end-to-end encryption;
cross-org/verifiable comms.
- Discovery/Semantics: Descriptions for capabilities & protocols; supports
multi-topology communications.
- Typical Strengths: strong identity, E2E privacy, cross-organization trust,
highest answer discovery rate.
- Typical Costs: DID/keys lifecycle adds integration/ops complexity; ecosystem
still maturing; UI/multimodal not first-class; slowest recovery.
- Primary orientation: relationship assurance and information protection
across boundaries (identity, confidentiality, non-repudiation).
- Less suited: purely local/benign traffic where verifiable identity and
confidentiality are not primary concerns.

-------------------------------------------3) Protocol Selection Task
-------------------------------------------
**Scenario Description:**
Multi-agent distributed document search system operating under cyclic fault
injection conditions. The system must maintain high answer discovery rates
while minimizing recovery time during agent failures. Agents are organized in
a mesh topology where 3 out of 8 agents are killed every 120 seconds,
requiring rapid fault detection, recovery, and service restoration.

**Module Details:**
**Module 1: Fault-Tolerant Document Search Network**
- Agents: Agent-1, Agent-2, Agent-3, Agent-4, Agent-5, Agent-6, Agent-7,
Agent-8
- Protocol Selection: Choose 1 protocol(s) from A2A, ACP, Agora, ANP

**Tasks:**
- Perform distributed document fragment search across 8 agents in mesh
topology.
- Maintain collaborative retrieval with TTL-based message forwarding and ring
communication.
- Detect agent failures through heartbeat monitoring (10s intervals, 30s
timeout).
- Execute rapid reconnection and service restoration after fault injection.
- Preserve answer discovery capability during 3-agent simultaneous failures.
- Support coordinator-worker communication for result aggregation.
- Handle cyclic fault patterns with 120s intervals over extended runtime
(1800s).

**Potential Issues:**

```

39


```
 - Simultaneous failure of 37.5% of agents (3/8) every 120 seconds.
 - Network partitions during fault injection causing message loss.
 - Recovery time bottlenecks affecting overall system availability.
 - Duplicate work during recovery phases reducing efficiency.
 - Answer quality degradation under reduced agent availability.
 - Heartbeat timeout false positives during network jitter.
 - Reconnection storms when multiple agents recover simultaneously.
 - TTL exhaustion in message forwarding during network instability.

 **Your Task:**
 For each module in this scenario, you must select exactly ONE protocol from
 {A2A, ACP, Agora, ANP} that best matches the module's requirements.

 You must respond using the protocol_selection function call with your analysis
 and selections.

```

G.10.2 Streaming Queue Router Prompt





40


```
- Typical Costs: less emphasis on UI capability negotiation; moderate recovery
performance.
- Primary orientation: structured, addressable operations with clear progress
semantics and repeatable handling at scale.
- Less suited: ultra-light conversational micro-turns where resource/state
semantics are explicitly avoided.

Agora (Meta-Protocol)
- Positioning: Minimal "meta" wrapper; sessions carry a protocolHash binding
to a plain-text protocol doc.
- Performance: avg 7.10-9.00s response, 6.1s recovery time, 60.0% success rate
- Discovery: wellknown returns supported protocol hashes; natural language is
a fallback channel.
- Evolution: Reusable "routines"; fast protocol evolution and heterogeneity
tolerance.
- Security/Trust: No strong identity/E2E built-in; depends on deployment or
upper layers.
- Typical Strengths: lightweight, negotiation-friendly, highly adaptable for
research/decentralized experiments, balanced recovery.
- Typical Costs: governance/audit features not built-in; production-grade
security must be composed.
- Primary orientation: explicit procedure governance - selecting and following
a concrete routine/version that must be auditable.
- Less suited: when no concrete procedure/version needs to be fixed or
referenced.

ANP (Agent Network Protocol)
- Positioning: Network & trust substrate for agents; three layers:
identity+E2E, meta-protocol, application protocols.
- Performance: avg 4.78-6.76s response, 10.0s recovery time (slowest), 61.0%
success rate (highest), 22.0% answer discovery rate (highest)
- Security/Trust: W3C DID-based identities; ECDHE-based end-to-end encryption;
cross-org/verifiable comms.
- Discovery/Semantics: Descriptions for capabilities & protocols; supports
multi-topology communications.
- Typical Strengths: strong identity, E2E privacy, cross-organization trust,
highest answer discovery rate.
- Typical Costs: DID/keys lifecycle adds integration/ops complexity; ecosystem
still maturing; UI/multimodal not first-class; slowest recovery.
- Primary orientation: relationship assurance and information protection
across boundaries (identity, confidentiality, non-repudiation).
- Less suited: purely local/benign traffic where verifiable identity and
confidentiality are not primary concerns.

-------------------------------------------3) Protocol Selection Task
-------------------------------------------
**Scenario Description:**
High-throughput question-answering system designed for streaming queue
pressure testing. The system processes batches of questions (50 per batch)
across multiple worker agents coordinated by a central coordinator in star
topology. Primary focus is minimizing end-to-end latency while maintaining
acceptable reliability under concurrent load.

**Module Details:**
**Module 1: High-Throughput QA Processing Pipeline**
- Agents: Coordinator-1, Worker-1, Worker-2, Worker-3, Worker-4
- Protocol Selection: Choose 1 protocol(s) from A2A, ACP, Agora, ANP

**Tasks:**
- Coordinator loads question batches from JSONL dataset
(top1000_simplified.jsonl).

```

41


```
 - Dynamic load balancing across 4 worker agents using queue-based task
 distribution.
 - Workers process questions with LLM inference and return structured
 responses.
 - Maintain response time constraints (60s timeout) with retry mechanisms (max
 3 retries).
 - Collect and aggregate results with comprehensive performance metrics.
 - Support concurrent processing with batch sizes of 5 questions per worker.
 - Generate detailed performance reports including latency distribution and
 success rates.

 **Potential Issues:**
 - High concurrent load causing worker saturation and queue backups.
 - Network timeout errors under sustained throughput pressure.
 - Load imbalance between workers leading to processing bottlenecks.
 - Connection retry storms during network instability.
 - Response time variance affecting P95/P99 latency targets.
 - Worker failure during batch processing causing partial results loss.
 - Memory pressure from large question batches and response buffering.
 - Protocol overhead impacting raw throughput under high QPS scenarios.

 **Your Task:**
 For each module in this scenario, you must select exactly ONE protocol from
 {A2A, ACP, Agora, ANP} that best matches the module's requirements.

 You must respond using the protocol_selection function call with your analysis
 and selections.

```

G.10.3 ProtocolRouterBench Instruction Prompt





42


```
 - Integration: Minimal SDK expectations; straightforward REST exposure.
 - Primary orientation: structured, addressable operations with clear progress
 semantics at scale.
 - Less suited: ultra-light conversational micro-turns that avoid
 resource/state semantics.

 Agora (Meta-Protocol)
 - Positioning: Minimal meta wrapper; sessions carry a protocolHash bound to a
 plain-text protocol document.
 - Discovery: /.well-known returns supported protocol hashes; natural language
 as fallback.
 - Evolution: Reusable "routines"; fast protocol evolution and heterogeneity
 tolerance.
 - Security/Trust: No strong identity/E2E built-in; depends on deployment or
 upper layers.
 - Primary orientation: explicit procedure governance (choose and follow a
 concrete routine/version).
 - Less suited: when no procedure/version needs to be fixed or referenced.

 ANP (Agent Network Protocol)
 - Positioning: Network & trust substrate; three layers: identity+E2E,
 meta-protocol, application protocols.
 - Security/Trust: W3C DID identities; ECDHE-based end-to-end encryption;
 cross-org/verifiable comms.
 - Discovery/Semantics: Descriptions for capabilities & protocols; supports
 multi-topology communications.
 - Primary orientation: relationship assurance across boundaries (identity,
 confidentiality, non-repudiation).
 - Less suited: benign/local traffic where verifiable identity and
 confidentiality are not primary concerns.

 ------------------------------------------- 2) Protocol Selection Task
 ------------------------------------------- **Scenario Description:** {scenario_description}
 **Module Details:** {module_details}

 **Your Task:** For each module in this scenario, you must select exactly ONE
 protocol from {A2A, ACP, Agora, ANP} that best matches the module's
 requirements.
 You must respond using the protocol_selection function call with your analysis
 and selections (machine-checkable JSON only).

```

G.10.4 ProtocolRouterBench Instruction Prompt(Spec + Perf)



43


```
- Security/Trust: Enterprise authN/Z; E2E not default (optional via outer
layers).
- Integration: Complements MCP; broad ecosystem.
- Orientation: sustained agent interaction and lightweight turn-taking.

ACP (Agent Communication Protocol)
- Transport/Model: REST-first; MIME multimodality; async-first with streaming.
- Discovery: Agent Manifest; single/multi-server topologies.
- Security/Trust: Web auth patterns; E2E not native.
- Integration: Minimal SDK; easy REST wrapping.
- Orientation: structured, addressable operations with clear progress
semantics.

Agora (Meta-Protocol)
- Positioning: Meta wrapper; session binds to a protocolHash referencing a
routine document.
- Discovery: /.well-known hashes; NL fallback.
- Security/Trust: Depends on deployment; no strong identity/E2E built-in.
- Orientation: explicit routine/version governance and auditability.

ANP (Agent Network Protocol)
- Positioning: Identity+E2E substrate; meta-protocol; application protocols.
- Security/Trust: W3C DID; ECDHE E2E; cross-org/verifiable communications.
- Orientation: boundary-crossing identity/confidentiality/non-repudiation.
