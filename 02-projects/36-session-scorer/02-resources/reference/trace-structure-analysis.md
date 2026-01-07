# Trace Structure Analysis

**Phase**: 2.2-2.6 (Trace Structure Discovery)
**Date**: 2026-01-05

---

## Key Finding: Data Hierarchy

```
Session
  └── Trace (1:N relationship via sessionId)
        └── Observation (1:N relationship via traceId)
```

**Important API Behavior**:
- `GET /sessions/{id}` returns traces WITHOUT observations
- `GET /traces/{id}` returns trace WITH observations
- `GET /observations` returns observations without trace context

To get full session data with observations, you must:
1. Get session (returns traces)
2. For each trace, get trace details (includes observations)

---

## Session Structure

**Fields from get-session API**:
| Field | Type | Description |
|-------|------|-------------|
| id | string | 32-char hex (MD5 hash) |
| createdAt | datetime | ISO 8601 timestamp |
| projectId | string | Langfuse project identifier |
| environment | string | Usually "default" |
| traces | array | Array of trace objects |

**Sample Session Stats**:
| Session | Traces | JSON Size | Notes |
|---------|--------|-----------|-------|
| Small (1c96db43...) | 8 | 94 KB | Short conversation |
| Medium (8172830f...) | 14 | 132 KB | Moderate conversation |
| Large (5ff25b22...) | 100* | 291 KB | Long conversation |

*Note: Large session shows 100 traces, may be paginated

---

## Trace Structure

**Fields from trace listing**:
| Field | Type | Description |
|-------|------|-------------|
| id | string | UUID format |
| projectId | string | Project identifier |
| name | string | Always "claude_code_user" |
| timestamp | datetime | When trace was created |
| userId | string | User email address |
| sessionId | string | Links to session |
| input | object/string | User message or tool output |
| output | null | Not captured by current tracing |
| metadata | object | Rich context (see below) |
| observations | array | Included only via get-trace |
| totalCost | number | Included only via get-trace |

**Trace Metadata Fields**:
| Field | Description | Example |
|-------|-------------|---------|
| project | Nexus project path | "c//Users/.../nexus/..." |
| conversationId | UUID for conversation | "7f1505c7-adf2-..." |
| gitBranch | Current git branch | "main" |
| cwd | Working directory | "c:\Users\..." |
| messageType | Type of message | "user" |
| source | Trace source | "claude_code_automatic" |

---

## Observation Structure

**All observations in sample are type GENERATION**

**Key Fields**:
| Field | Type | Description |
|-------|------|-------------|
| id | string | UUID |
| traceId | string | Parent trace UUID |
| type | string | "GENERATION" (only type seen) |
| name | string | "claude_response" |
| model | string | "claude-sonnet-4-5-20250929" |
| input | null | Not captured |
| output | string | Claude's response with tool calls |
| latency | number | Response time (ms) |
| usageDetails | object | Token breakdown |
| costDetails | object | Cost breakdown |

**Usage/Cost Details**:
```json
{
  "usageDetails": {
    "output": 243,
    "total": 243
  },
  "costDetails": {
    "output": 0.003645,
    "total": 0.003645
  },
  "promptTokens": 0,
  "completionTokens": 243,
  "totalTokens": 243
}
```

**Note**: `promptTokens` is always 0, only output tokens are tracked. This appears to be a limitation of the claude-langfuse-monitor bridge.

---

## Statistics (100 Observation Sample)

| Metric | Value |
|--------|-------|
| Total tokens | 58,809 |
| Total cost | $0.8821 |
| Avg tokens/observation | 588 |
| Avg cost/observation | $0.0088 |
| Models used | claude-sonnet-4-5-20250929 |

---

## Input Content Types

From analyzing trace inputs, messages fall into categories:

1. **Skill Loading**: Full SKILL.md content injected
   - Large JSON objects with skill metadata
   - Can be 10-20KB per trace

2. **Web Search Results**: Tool output from WebSearch
   - Contains search results with URLs and snippets
   - Reminder appended about citation

3. **System Messages**: TodoWrite confirmations, etc.
   - Small messages like "Todos have been modified successfully"

4. **User Messages**: Direct user input
   - Typically shortest inputs

---

## Observations Not Found

The Claude Code tracing only captures:
- GENERATION observations (LLM responses)

Not captured (would need OTEL enrichment):
- Tool calls as separate SPAN observations
- File reads/writes as observations
- Token costs for input (only output tracked)

---

## Implications for Scoring

1. **Session-level scoring** is feasible
   - Can aggregate across all traces in a session
   - Need to fetch each trace individually for observations

2. **Trace-level scoring** is natural
   - Each trace = 1 user turn
   - Has clear boundaries

3. **Observation-level scoring** limited
   - Only GENERATION type available
   - No tool call breakdown

4. **Cost analysis possible**
   - Output tokens and cost are tracked
   - Input tokens NOT tracked (limitation)

5. **Context efficiency** hard to measure
   - Input tokens not captured
   - Can estimate from input JSON size

---

## Open Questions Resolved

- [x] What is 1 trace? = 1 user message + response cycle
- [x] How do sessions group traces? = Via sessionId field
- [x] What's in observations? = GENERATION type with LLM response
- [x] What metadata is available? = project, conversationId, gitBranch, cwd

## Questions Remaining

- [ ] Why are input tokens always 0?
- [ ] Can we enrich OTEL tracing to capture tool calls?
- [ ] How to handle very large sessions (pagination)?

---

*Next: Phase 3 - Size & Complexity Analysis*
