<!-- Source: 07-ProtocolBench-2510.17149.pdf | Chunk 5/8 -->

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


**Scoring and missingness.** Scenario accuracy equals 1 only if all modules are correctly
predicted. Module accuracy is the fraction of correctly predicted modules. If a module
record is malformed or absent, the entire scenario is list-wise excluded and the exclusion is
logged; no zero-filling.


**Train/dev/test policy.** This release ships only the 60 evaluation scenarios. A stratified
split will be added in a future release.


**Non-leakage and pre-specification.** All texts are model-generated with human curation.
Vendor, product, and library names are removed or neutralized; only generic capabilities
and interaction semantics remain. The decision rules, prompts, and schema are pre-specified
and version-anchored.


E.3.3 Artifacts


We release configs, scripts, commit hashes, dashboards, dataset splits, execution logs, and
the full ProtocolBench bundle. A one-shot script reproduces the entire pipeline (scenarios
_→_ decisions _→_ metrics _→_ tables). The manifest records file hashes and commits.


21


E.4 Threats to Validity, Ablations, and Statistical Procedures


E.4.1 Construct validity and multi-implementation check


We separate protocol design from implementation artifacts. A planned multiimplementation comparison (production-optimized vs. minimal references) is run under
identical adapters; we expect relative orderings to remain stable.


E.4.2 Ablations


1. **Envelope-only vs. full-feature paths:** disable advanced features and compare
against full stacks.


2. **Topology substitution:** freeze GAIA’s dynamic star and compare to the default
dynamic configuration.


3. **Planner freezing:** fix planner outputs to isolate protocol effects.


4. **ProtocolBench-specific:** remove lock/exclude phrases to quantify A2A _↔_ ACP
confusions; disable `priority_decide()` to observe tie instability.


E.4.3 Statistical procedures


For continuous metrics we compute BCa bootstrap 95% CIs with _B_ =10 _,_ 000 resamples. ProtocolBench accuracies use exact binomial or Wilson intervals. Pairwise comparisons report
Cliff’s _δ_ and Hodges–Lehmann median differences (point estimate with 95% CI). Multiple


22


comparisons are corrected via Holm–Bonferroni. We separate _in-run jitter_ (per-request coefficient of variation) from _run-to-run variability_ (across-run coefficient of variation) when
repeated runs are available.


F Scenario Prompt design


**FS Shard Worker System Prompt** is used by fail-storm shard workers to maximize
answer discovery under cyclic faults.



23


```
 CRITICAL: When in doubt, ALWAYS choose found=true! It's better to be overly
 generous than to miss relevant information.

 ANSWER EXTRACTION:
 When found=true, extract the most relevant information:
 - Include specific facts, names, dates, numbers
 - Provide context that helps answer the question
 - Be specific and detailed rather than vague

 LIBERAL DETECTION EXAMPLES:
 ..."""

```

**FS Local Search Prompt** guides generous local matching to maximize discovery before
neighbor/ring forwarding.



24


```
 Remember: It's better to find partial information than to miss relevant
 content. The collaborative system will combine partial answers from multiple
 agents."""

```

**SQ QA Worker System Prompt** is designed for high-throughput QA workers under star
topology.





**SQ Meta Coordinator Task Prompt** describs the streaming pressure test objective and
constraints.







**GAIA Planner Prompt** defines a task analysis system that classifies a task, assesses
complexity, selects tools, and configures specialized agents with roles. It enforces rules and
provides a few-shot JSON example to guide structured multi-agent planning.







25


```
  - high: Complex tasks requiring 6+ steps, domain expertise, or
  sophisticated reasoning

3. REQUIRED TOOLS - Select from available tools:
  Available tools: {available_tools}

4. AGENT CONFIGURATION - For each required tool, specify:
  - name: Descriptive agent name (e.g., "WebResearcher", "DataAnalyst",
  "CodeExecutor")
  - role: Create meaningful, task-specific roles (e.g.,
  "information_gatherer", "computational_specialist", "data_processor",
  "final_synthesizer", "document_analyzer", "web_navigator", etc.)
  - Be creative with roles - they should reflect the agent's specific
  function in solving the task

  Example role types you can use as inspiration:
  * information_gatherer: Searches for and collects relevant information from
  various sources
  * computational_specialist: Executes calculations, data processing, and
  analytical tasks
  * document_analyzer: Processes and extracts information from documents and
  files
  * evidence_synthesizer: Integrates information from multiple sources into
  coherent conclusions
  * task_coordinator: Breaks down complex tasks and manages workflow
  execution
  * content_creator: Generates reports, summaries, and structured outputs
  * domain_expert: Provides specialized knowledge in specific fields
  * data_processor: Handles data transformation, cleaning, and formatting
  * web_navigator: Specializes in web search and online information retrieval
  * final_synthesizer: Provides comprehensive final answers and conclusions

5. DOMAIN EXPERTISE needed (technology, science, business, finance,
healthcare, etc.)

6. PROCESSING REQUIREMENTS:
  - Sequential vs parallel processing needs
  - Validation/verification requirements
  - Error handling complexity

IMPORTANT HARD RULES:
- The tool 'create_chat_completion' is reserved for the FINAL agent only.
Include it exactly once and position it as the LAST step in the workflow. Do
NOT assign or call it in intermediate steps or by non-final agents.

IMPORTANT: Based on the GAIA task level {level}, we recommend using
approximately {recommended_agents} agents for optimal performance. However,
you can adjust this number based on task complexity:
- Use fewer agents (1-2) for very simple, single-step tasks
- Use the recommended number ({recommended_agents}) for typical level {level}
tasks
- Use more agents (up to {max_agents}) only if the task genuinely requires
complex multi-step processing

You must limit your agent recommendations to a maximum of {max_agents} agents
total. Plan efficiently within this constraint.
Respond with detailed JSON analysis including your reasoning.

Analyze the task and respond with a JSON object containing:
{{
 "task_type":
 "general_qa|research_task|computational_task|multi_step_analysis",
 "complexity": "low|medium|high",

```

26


```
  "required_tools": ["tool1", "tool2"],
  "agents": [
    {{
     "tool": "tool_name",
     "name": "AgentName",
     "role": "specific_role_based_on_function",

    }}
  ],
  "estimated_steps": number,
  "domain_areas": ["domain1", "domain2"]
 }}

 Example:
 {{
  "task_type": "research_task",
  "complexity": "medium",
  "required_tools": ["browser_use", "create_chat_completion"],
  "agents": [
    {{
     "tool": "browser_use",
     "name": "WebResearcher",
     "role": "academic_information_gatherer",

    }},
    {{
     "tool": "create_chat_completion",
     "name": "ReasoningSynthesizer",
     "role": "evidence_synthesizer",

    }}
  ],
  "estimated_steps": 3,
  "domain_areas": ["general_knowledge"]
 }}
 """

```

**Agent Role template** instantiates agent expertise, responsibilities, and collaboration,
ensuring structured coordination and quality outcomes in multi-agent systems.


**LLM Judge Prompt** provides the LLM with a process-oriented evaluation framework
emphasizing a consistent, rubric-based assessment to ensure transparent and reproducible
scoring. To thoroughly evaluate the MAS’s communication process as well as the final
answer, full execution logs are prioritized over summaries as they provide the necessary
unabridged evidence.


27


28


```
  - Communication is incomplete or incorrect, tools are misused, or agents
  fail to share necessary details.

 - **Score 1 (Very Poor):**
  - No meaningful communication, hallucinated tool use, or completely
  irrelevant traces.

 -- **RESPONSE FORMAT:**

 Respond with a single JSON object. Do not include any other text or
 explanations outside the JSON.
 {{
  "is_correct": true/false,
  "quality_score": 1-5,
  "reasoning": "Detailed explanation for your judgment. Justify BOTH the
  correctness of the final answer and the quality score based on the process
  trace and the rubric.",
  "answer_quality": "excellent/good/fair/poor",
  "final_answer_present": true/false,
  "partial_credit": 0.0-1.0
 }}

 Be thorough but fair in your evaluation. Provide specific reasoning for your
 judgment.
 """

```

G ProtocolRouter Technical Details


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


