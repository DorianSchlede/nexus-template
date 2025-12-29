<!-- Source: 07-ProtocolBench-2510.17149.pdf | Chunk 8/8 -->

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

-------------------------------------------2) Protocol performance in some scenarios
-------------------------------------------[
 {
  "id": "G1-QA",
  "description": "GAIA hierarchical DocQA with planning, explicit
  workflow/message-flow, sandboxed tools, step memory, and LLM judging.",
  "modules_count": 1,
  "module": [
   {
    "name": "Hierarchical DocQA Pipeline",
    "agents":
    ["Planner","Reader/Extractor","Aggregator/Summarizer","Judge"],
    "protocol_selection": {"choices": ["A2A","ANP","ACP","Agora"],
    "select_exactly": 1},
    "tasks": [
     "Emit machine-readable manifest (roles, tools, workflow).",
     "Run P2P serving with explicit message-flow.",
     "Record step-based memory with timestamps and tool-call traces.",
     "Summarize and judge quality; emit metrics."
    ],
    "potential_issues": [
     "Long-running tasks with streaming outputs/partials.",
     "Out-of-order or retried deliveries under concurrency.",
     "Auditability and replay of full execution log.",
     "Cross-run fairness (identical seed/config)."
    ]
   }
  ],
  "experiment_results": {
   "quality_avg": {"acp": 2.27, "a2a": 2.51, "anp": 2.14, "agora": 2.33,
   "meta": 2.50},
   "success_avg": {"acp": 5.25, "a2a": 9.29, "anp": 7.28, "agora": 6.27,
   "meta": 9.90},
   "single_task_comm_time@5_example": {
    "a2a_ms": [25.38, 20.64, 28.19, 21.65, 21.36],
    "acp_ms": [15.30, 13.64, 14.75, 16.22, 12.75],
    "anp_ms": [39.01, 54.74, 27.60, 21.86, 34.48],

```

44


```
   "agora_ms": [29.30, 21.83, 30.49, 22.41, 35.50]
  }
 }
},
{
 "id": "S1-Queue",
 "description": "Streaming Queue: centralized 5-agent network; 1000 items;
 pressure test for speed and stability.",
 "modules_count": 1,
 "module": [
  {
   "name": "Coordinator-Workers Streaming Queue",
   "agents": ["Coordinator","Worker-1","Worker-2","Worker-3","Worker-4"],
   "protocol_selection": {"choices": ["A2A","ANP","ACP","Agora"],
   "select_exactly": 1},
   "tasks": ["Load-balance tasks","Track per-task latency and
   completion","Minimize worker variance","Measure
   errors/retries/timeouts"]
  }
 ],
 "experiment_results": {
  "performance": {
```

`"A2A": {"total":1000,"duration_s":2427,"avg_ms":9698,"min_ms":6938,"m` _⌋_
```
   ax_ms":15129,"std_ms":1127},
```

`"ACP": {"total":1000,"duration_s":2417,"avg_ms":9663,"min_ms":6881,"m` _⌋_
```
   ax_ms":14235,"std_ms":1077},
```

`"ANP": {"total":1000,"duration_s":2843,"avg_ms":11364,"min_ms":243,"m` _⌋_
```
   ax_ms":50104,"std_ms":5732},
```

`"Agora":{"total":1000,"duration_s":3298,"avg_ms":13135,"min_ms":524,"` _⌋_
```
   max_ms":28213,"std_ms":5089}
  }
 }
},
{
 "id": "F1-Storm",
 "description": "Fail Storm on ring-structured Shard QA; randomly kill 3
 agents every 2 minutes; measure recovery and pre/post metrics.",
 "modules_count": 1,
 "module": [
  {
   "name": "Shard QA with Fault Injection",
   "agents": ["QA-1","QA-2","QA-3","QA-4","QA-5","QA-6","QA-7","QA-8"],
   "protocol_selection": {"choices": ["A2A","ANP","ACP","Agora"],
   "select_exactly": 1}
  }
 ],
 "experiment_results": {
  "performance": [
```

`{"protocol":"ACP",` `"answer_found_pct_pre":14.76,"answer_found_pct_po` _⌋_
`st":13.64,"steady_latency_s_pre":4.3776,"steady_latency_s_post":4.185` _⌋_
```
   1,"recovery_s":8.0482},
```

`{"protocol":"A2A",` `"answer_found_pct_pre":14.74,"answer_found_pct_po` _⌋_
`st":14.57,"steady_latency_s_pre":4.3399,"steady_latency_s_post":4.185` _⌋_
```
   5,"recovery_s":8.0027},
```

`{"protocol":"ANP",` `"answer_found_pct_pre":14.88,"answer_found_pct_po` _⌋_
`st":12.94,"steady_latency_s_pre":4.3428,"steady_latency_s_post":4.182` _⌋_
`6,"recovery_s":8.0033},{"protocol":"AGORA","answer_found_pct_pre":14.` _⌋_
`91,"answer_found_pct_post":12.12,"steady_latency_s_pre":4.3311,"stead` _⌋_
```
   y_latency_s_post":4.1799,"recovery_s":8.0026}
  ]
 }
},
{
 "id": "M1-Doctors",

```

45


```
  "description": "Doctor-to-doctor dialogue system with two legitimate LLM
  agents; multi-round consultations.",
  "modules_count": 1,
  "module": [
   {
    "name": "Doctor-Doctor Dialogue System",
    "agents": ["Doctor A","Doctor B"],
    "protocol_selection": {"choices": ["A2A","ANP","ACP","Agora"],
    "select_exactly": 1}
   }
  ],
  "experiment_results": {
```

`"safety_matrix": [` `{"protocol":"Agora","tls_transport":true,"ses` _⌋_
`sion_hijack_protection":true,"e2e_detection":false,"packet_tunnel_prote` _⌋_
```
   ction":true,"metadata_exposure_protection":true},
```

`{"protocol":"ANP",` `"tls_transport":true,"session_hijack_protection":` _⌋_
```
    true,"e2e_detection":true,
    "packet_tunnel_protection":true,"metadata_exposure_protection":true},
```

`{"protocol":"ACP",` `"tls_transport":false,"session_hijack_protection"` _⌋_
```
    :true,"e2e_detection":true,
    "packet_tunnel_protection":false,"metadata_exposure_protection":true},
```

`{"protocol":"A2A",` `"tls_transport":false,"session_hijack_protection"` _⌋_
```
    :true,"e2e_detection":true,
    "packet_tunnel_protection":false,"metadata_exposure_protection":true}
   ]
  }
 }
]

-------------------------------------------3) Protocol Selection Task
-------------------------------------------**Scenario Description:** {scenario_description}
**Module Details:** {module_details}

IMPORTANT: Provide a selection for EVERY module. Use the protocol_selection
function call with analysis and selections (machine-checkable JSON only).

```

46


