<!-- Source: 07-ProtocolBench-2510.17149.pdf | Chunk 6/8 -->


This section specifies the ProtocolRouterin full detail, covering the unified API, field alignment, transport and interaction semantics, reliability and ordering guarantees, identity and
security, conformance testing, and known limitations. The description corresponds 1:1
to the implementation of `BaseAgent`, `BaseProtocolAdapter` and its concrete subclasses
( `A2AAdapter`, `ACPAdapter`, `ANPAdapter`, `AgoraClientAdapter` ). The final subsection replaces the previous router notes with a complete, self-contained router specification that
sits _above_ PAL and uses the same universal message envelope.


G.1 Unified Interface Specification


**Roles and objects.**


- **BaseAgent (dual role)** : Acts as a server (receives messages) and as a multiclient (sends to multiple destinations via multiple protocols). Server responsibilities are provided by `BaseServerAdapter` implementations (e.g., `A2AServerAdapter`,
`AgentProtocolServerAdapter`, `ACPServerAdapter`, `ANPServerAdapter` ). The execution entry point is SDK-native, e.g., `async def execute(context, event_queue)` .


- **BaseProtocolAdapter (egress abstraction)** : One adapter instance per egress edge
(destination/URL/credentials) for isolation and precise metering. Each adapter encapsulates encoding/decoding, transport, auth, and feature negotiation for a single protocol
and destination.


**Unified send/receive API and lifecycle.**





29


- **send_message** : Sends a protocol-specific payload and returns the protocol response.
PAL unifies encoding/decoding via the UTE (Unified Transport Envelope).


- **send_message_streaming** (optional): Yields protocol events/chunks as a stream
(e.g., SSE).


- **receive_message** : Typically a no-op for client adapters; ANP can poll an inbound
session queue.


- **initialize/health_check/cleanup** : Capability discovery/priming (cards/manifests),
readiness checks, and resource teardown.


**Unified Transport Envelope (UTE).**





Minimal required fields: `src`, `dst`, `content`, `context` . In `BaseAgent.send()`, `UTE.new(...)`
produces the envelope that `ENCODE_TABLE[protocol_name]` transforms into protocol payload; responses are converted back via `DECODE_TABLE` into a UTE, and upper layers consume
`ute_response.content` .


**Async event model and hooks (recommended).**


- _before_encode / after_encode_ : UTE _→_ protocol payload, pre/post.


- _before_transport / after_transport_ : Network send/receive, pre/post.


- _on_stream_event_ : Streaming fragment/event callback.


- _on_retry / on_backoff_ : Retry and backoff callbacks.


- _on_decode / on_error_ : Protocol response decoding and normalized error handling.


Unified metrics (e.g., `REQUEST_LATENCY`, `REQUEST_FAILURES`, `MSG_BYTES` ) are labeled by
`(src_agent, dst_id, protocol)` . `MSG_BYTES` reports the byte length of the serialized
protocol payload.


**Unified error taxonomy.** Adapter exceptions are normalized by PAL into: `E_TIMEOUT`,
`E_HTTP`, `E_CONN`, `E_PROTOCOL`, `E_ENCODE/DECODE`, `E_UNSUPPORTED` . PAL increments failure
counters and re-raises so routing/network layers can decide on retries or failover.


G.2 Message/Event Field Alignment (A2A/ACP/ANP/AGORA _→_ UTE)


Table 8 aligns key fields on the send path (UTE _→_ protocol). Paths use an English `JSONPath` like notation.


30


Table 8: UTE to protocol field alignment (send path).



**UTE Field** **A2A (/message) ACP**
**(/acp/mes-**
**sage)**



**ANP** **(/an-**
**p/message** **/**
**WS)**



**AGORA (task)**



_Shorthand: In the ANP column, leading ”payload.”_ _is omitted._ _In the ACP/AGORA columns,_
_leading ”metadata.” is omitted when applicable._

```
id request.id id request_id request_id
src params.- sender source_id / source
       routing.source session DID

```

```
dst params.       routing.       destination

```

```
receiver target_did / target (URL)
         session

```

```
content params.message payload payload message /
                                  parameters
trace_id params.- trace_id trace_id trace_id
       context.       trace_id

```

```
idempotency params.       context.       idempotency_key

```

```
correlation_id
or
idempotency_key

```

```
idempotency_key idempotency_key

```

```
stream HTTP Accept: stream=true / WS persistent by type /
       event-stream SSE stream task
session_id params.- session_id connection / session
       context.- session
       session_id
meta.protoc passthrough passthrough enables influences task
                         meta-protocol

```


**Reserved/extension** **notes.** A2A exposes authenticated cards; ACP provides
`/acp/capabilities` and `/acp/status` ; ANP carries `protocol_type` (META/APPLICATION/NATURAL) and DID/WS semantics; AGORA registers routines via task
decorators.


G.3 Transport and Interaction Semantics


**Sync/async and streaming.**


- **A2A** : HTTP sync `POST /message` ; obtain SSE via `Accept:` `text/event-stream` .


- **ACP** : HTTP sync `POST /acp/message` ; SSE supported; long-running jobs via
`/acp/status` polling.


- **ANP** : WebSocket persistent sessions ( `SimpleNodeSession` ); HTTP fallback `POST`
`/anp/message` for local/testing.


- **AGORA** : Official SDK task model or simplified `POST /agora` for single-round conversations and `POST /conversations/conversationId` for multi-round conversations.


**Long-running job state.** Native support priority: ACP (status endpoint) _>_ A2A (SSE
increments/custom heartbeats) _≈_ ANP (session heartbeats/app-level receipts) _>_ AGORA
(task-level receipts). PAL recommends `context.session_id` and `idempotency_key` as anchors for idempotency and resumption.


**Artifact** **handling.** Inline artifacts if _<_ 1 MB in `content` ; otherwise reference via
`context.artifact_refs` (e.g., `s3://` or pre-signed URLs). ANP/WS can send binary
frames; for HTTP, prefer chunking or external links to avoid `max_message_size` limits.


G.4 Reliability and Ordering Guarantees


**Retry/backoff and deduplication.** PAL does not implicitly retry; routing/network layers
decide based on error category. Idempotency is propagated via `context.idempotency_key`


31


and mapped to protocol fields. Servers/business logic should implement deduplication on
arrival.


**Ordering and replay.**


- **HTTP (A2A/ACP)** : Transport is unordered; applications should reorder using
`seq` / `trace_id` .

- **ANP (WS)** : Within a single session, ordering is approximately sequential; across sessions/links, merge at the application layer. For SSE, `Last-Event-ID` enables replay if
supported by the server.


**Normalized error mapping (examples).**


- `httpx.TimeoutException` _→_ `E_TIMEOUT`

- `httpx.HTTPStatusError` _→_ `E_HTTP` (status code and summary included)

- WS handshake/DID resolution failure _→_ `E_CONN`

- `json.JSONDecodeError` _→_ `E_DECODE`

- Missing/unsupported capability _→_ `E_UNSUPPORTED`


G.5 Identity and Security


**Authentication/authorization.**


- **HTTP** **(A2A/ACP/AGORA)** : `Authorization:` `Bearer <token>` ; recommend
mTLS at gateway/reverse proxy; `/.well-known/agent.json` may expose capabilities
and endpoints; A2A supports authenticated cards.

- **ANP (DID)** : `did:wba` identities; local/remote DID creation and resolution. Test setups
may enable verification bypass for interoperability; production must enforce strict publickey validation and DID document checks.


**End-to-end confidentiality (E2E).** ANP uses ECDHE + AES-GCM for transparent persession encryption. For HTTP protocols, use TLS/mTLS; optionally add application-layer
encryption for `content` when regulatory or cross-tenant constraints apply.


**Trust anchors and certificate chains.** HTTP relies on public or private root CAs. DID
trust anchors are the method and resolver service; cache DID documents (TTL/expiry
policy) and support key rotation/revocation.


G.6 Adapter Conformance Testing


**Per-protocol test suite (capability** _×_ **protocol).**


1. **Basic connectivity** : `initialize()` fetches cards/capabilities (A2A/ACP/AGORA),
ANP establishes DID/session; `health_check()` returns true.
2. **Single round trip** : UTE _↔_ protocol encode/decode consistency (field fidelity, nullhandling policy, case conventions).
3. **Streaming** : SSE/WS event ordering, boundaries, termination (including empty lines
and `data:` prefix); interruption/resume behavior.
4. **Long-running** : ACP `/acp/status` vs. A2A/ANP heartbeats/progress; resumption
keyed by `session_id` .
5. **Security/auth** : Rejection on missing/invalid credentials; card access control; DID failures and certificate expiry.
6. **Edge cases** : Large messages (near `max_message_size` ), high concurrency, network jitter, server 4xx/5xx/malformed JSON.


**Regression corpus and coverage.**


- Maintain stable wire-contract fixtures per protocol (request/response/event fragments)
as baselines.


32


- Achieve coverage across encode/decode, error, and streaming branches.


- Fix load-test baselines and concurrency; report P50/P95/P99 and jitter coefficient
(std/mean).


**Known limitations and notes.**


- **A2AAdapter** : `/inbox` is not universally implemented (PAL keeps a negative cache);
`receive_message()` is a compatibility stub.


- **ACPAdapter** : Streaming depends on server SSE; long-running flows require
`/acp/status` .


- **ANPAdapter** : Test configs may enable DID verification bypass; if no DID service is
available, use HTTP fallback `POST /anp/message` ; the local resolver caches target DIDs
and is not a general-purpose resolver.


- **AgoraClientAdapter** : Without official `toolformer`, uses simplified HTTP with keyword classification; semantics and performance are limited.


- **Local loopback** : `IntelligentAgentNetwork._execute_single_agent_task()` may
use `agent.send(agent_id, ...)` for self-delivery; the network must bind an explicit
`default` adapter for that `agent_id` or provide a loopback route.


- **Ordering** : HTTP is not ordered; ANP is near-ordered per session; cross-session requires
merge logic.


- **Idempotency/dedup** : Client adapters do not persist deduplication; implement on the
server or one layer up.


G.7 Common Endpoints and Sample Requests (capture reference)


**A2A.**


- `GET /.well-known/agent.json`


- `GET /health`


- `POST /message`

```
{"id":"<uuid>","params":{"message":{"text":"..."},
"context":{"trace_id":"..."},
"routing":{"destination":"agent_B","source":"agent_A"}}}

```

**ACP.**


- `GET /.well-known/agent.json`


- `GET /acp/capabilities`


- `GET /acp/status`


- `POST /acp/message`

```
{"id":"<uuid>","type":"request","sender":"agent_A",
"receiver":"agent_B", "payload":{"text":"..."},
"timestamp":1730000000.0,"correlation_id":"<uuid>",
"metadata":{"trace_id":"..."}}

```

**ANP.**


- WS: `ws(s)://<host>:<port>/ws`


- HTTP fallback: `POST /anp/message`

```
{"type":"anp_message","request_id":"<uuid>",
"payload":{"text":"...","context":{"trace_id":"..."}},
"timestamp":1730000000.0, "source_id":"anp_client"}

```

33


**AGORA.**


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

