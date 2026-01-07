# Langfuse Trace Mapping for Subagents

**Discovered**: 2026-01-07
**Project**: 34-subagent-validation-system

---

## Key Finding: How to Identify Subagent Traces

### Identifiers Available

| Field | Source | Example | Uniqueness |
|-------|--------|---------|------------|
| `agentId` | Task tool response | `ac75a88` | Unique within conversation, may collide across time |
| `sessionId` | Langfuse trace | `db0745773b37d794...` | **Unique per subagent run** |
| `conversationId` | Langfuse metadata | `agent-ac75a88` | Contains agentId, queryable |
| `traceId` | Langfuse trace | UUID | Unique per API call/message |

### Recommended Approach

**Use `sessionId` as primary identifier** for subagent traces:

```python
# After spawning subagent, get its traces by agentId first
agent_id = "ac75a88"  # From Task tool response

# Find the subagent's Langfuse sessionId
for trace in langfuse.list_traces(limit=100):
    if trace.metadata.get('conversationId') == f"agent-{agent_id}":
        session_id = trace.sessionId
        break

# Store session_id for later retrieval
# This is the UNIQUE identifier for this subagent run
```

### Why Not Just agentId?

1. **agentId is short** (7 chars) - collision risk over time
2. **agentId is per-conversation** - same agentId could be reused in different parent sessions
3. **sessionId is guaranteed unique** by Langfuse

### Why Not Just conversationId?

1. **conversationId is derived from agentId** (`agent-{agentId}`)
2. Same collision risk as agentId
3. But useful for **querying** since it's in metadata

### Trace Structure

```
Parent Session (Claude Code)
├── sessionId: "main_session_hash"
├── conversationId: "uuid-parent-conversation"
│
└── Subagent 1 (Task tool)
    ├── agentId: "a7ac23a" (returned by Task tool)
    ├── sessionId: "3af6b55643f813c7..." (Langfuse unique)
    ├── conversationId: "agent-a7ac23a" (Langfuse metadata)
    └── traces: [trace1, trace2, ...] (multiple per conversation)
```

### Query Patterns

**Find subagent by agentId:**
```python
# Works for recent lookups
traces = [t for t in langfuse.list_traces()
          if t.metadata.get('conversationId') == f"agent-{agent_id}"]
```

**Get all traces for a subagent session:**
```python
# Once you have sessionId, get all traces
traces = langfuse.list_traces(session_id=session_id)
```

**Composite key for storage (RECOMMENDED):**
```python
# ALWAYS use composite key for uniqueness
unique_key = f"{session_id}:{agent_id}"

# Example: "db0745773b37d794:ac75a88"
# - session_id: Langfuse unique per subagent run
# - agent_id: Claude Code internal ID
# Together: guaranteed unique, traceable to both systems
```

---

## Timing Considerations

- **Ingestion delay**: ~5-10 seconds after subagent completes
- **Monitor required**: `claude-langfuse-monitor` must be running
- **Multi-trace**: A subagent conversation may produce multiple traces (one per turn)

---

## Implementation Recommendation

1. **Run subagent** → get `agentId` from Task tool response
2. **Wait 5-10s** for Langfuse ingestion
3. **Query by conversationId** → `metadata.conversationId == f"agent-{agentId}"`
4. **Extract sessionId** from first matching trace
5. **Store sessionId** as the canonical identifier for this run
6. **Later retrieval**: Query by `sessionId` to get all traces

---

*This document is the authoritative reference for subagent trace identification in Project 34.*
