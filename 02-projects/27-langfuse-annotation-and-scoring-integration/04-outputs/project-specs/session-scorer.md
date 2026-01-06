# Spawned Project: Session Scorer

**Parent Research**: Project 27 - Langfuse Annotation and Scoring Integration
**Estimated Effort**: Medium (3-5 sessions)
**Priority**: High (core scoring capability)
**Updated**: 2026-01-05 (Post-Validation Revision)

---

## Purpose

Build the core SessionScorer that uses Claude Code subagents (Task tool) to score any session across 6 dimensions (revised), handle large sessions via **token-based** chunking, and store results to Langfuse.

---

## Scope

### Must Do
1. Build `SessionScorer` skill using Claude Code subagents
2. Implement session fetching with observation retrieval
3. Implement **token-based** chunking (not trace-count based)
4. Extract task context from first user message for accurate scoring
5. Score 6 revised dimensions via subagent
6. Store scores to Langfuse via API
7. Calculate overall_quality weighted score

### Revised Dimensions (Post-Validation)
1. `task_completion` (CATEGORICAL) - weight 0.30
2. `execution_quality` (NUMERIC) - weight 0.25
3. `tool_mastery` (NUMERIC) - weight 0.20
4. `resource_efficiency` (NUMERIC) - weight 0.15
5. `security_compliance` (CATEGORICAL) - weight 0.05
6. `user_satisfaction` (CATEGORICAL) - weight 0.05

### Out of Scope
- Weekly automation (separate project)
- Human calibration workflow (separate project)
- Improvement suggestion generation (separate project)

---

## Dependencies

**Requires**:
- Score configs created in Langfuse (Project 28)
- Langfuse running at localhost:3002
- Anthropic API key for Claude calls

**Enables**:
- Weekly Analysis Workflow project
- Future specialized critic agents

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    SessionScorer                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  score_session(session_id: str) → SessionScores         │
│      │                                                   │
│      ├─► fetch_session_with_traces()                    │
│      │       └─► For each trace: fetch observations     │
│      │                                                   │
│      ├─► check_chunking_needed()                        │
│      │       └─► If >50 traces: split into chunks       │
│      │                                                   │
│      ├─► build_scoring_prompt()                         │
│      │       └─► Include traces, metadata, criteria     │
│      │                                                   │
│      ├─► call_claude_for_scoring()                      │
│      │       └─► Structured JSON output                 │
│      │                                                   │
│      ├─► aggregate_chunk_scores() (if chunked)          │
│      │       └─► Weighted avg / majority vote           │
│      │                                                   │
│      └─► store_scores_to_langfuse()                     │
│              └─► Create score for each dimension        │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Implementation Steps

### Phase 1: Session Fetcher

```python
class SessionFetcher:
    """Fetch sessions with full trace and observation data."""

    def fetch_session(self, session_id: str) -> Session:
        # 1. Get session metadata
        session = langfuse.get_session(session_id)

        # 2. Get all traces for session
        traces = langfuse.list_traces(session_id=session_id)

        # 3. For each trace, get observations (CRITICAL - not in session API)
        for trace in traces:
            trace.observations = langfuse.get_trace(trace.id).observations

        return Session(metadata=session, traces=traces)
```

### Phase 2: Token-Based Chunking (VALIDATED)

**Critical Fix**: Original strategy used 20 traces per chunk, which overflows context. Must use token-based chunking.

```python
# Validated configuration
TARGET_TOKENS = 70000   # Leave headroom for prompt + output
MIN_OVERLAP = 4         # 2 was insufficient for multi-turn context
MIN_CHUNK_RATIO = 0.5   # Merge small final chunks

def chunk_by_tokens(traces: List[Trace], target: int = TARGET_TOKENS) -> List[List[Trace]]:
    """Split session by TOKEN budget, not trace count.

    Key insight: 20 traces + observations = ~115k tokens = OVERFLOW
    """
    chunks = []
    current = []
    current_tokens = 0

    for trace in traces:
        trace_tokens = estimate_trace_tokens(trace)

        if current_tokens + trace_tokens > target and len(current) > MIN_OVERLAP:
            chunks.append(current)
            current = current[-MIN_OVERLAP:]  # Keep overlap for context
            current_tokens = sum(estimate_trace_tokens(t) for t in current)

        current.append(trace)
        current_tokens += trace_tokens

    # Handle final chunk - merge if too small
    if current:
        if chunks and len(current) < len(chunks[-1]) * MIN_CHUNK_RATIO:
            chunks[-1].extend(current[MIN_OVERLAP:])
        else:
            chunks.append(current)

    return chunks

def estimate_trace_tokens(trace: Trace) -> int:
    """Estimate tokens for trace + observations."""
    tokens = len(json.dumps(trace.input or {})) // 4
    for obs in trace.observations or []:
        tokens += len(obs.output or "") // 4 + 200
    return tokens
```

### Phase 3: Scoring Prompt

See `03-working/architecture-design.md` for full prompt template.

Key elements:
- Session context (ID, trace count, project, duration)
- Formatted traces with input/output
- Scoring criteria for each dimension
- Structured JSON output format

### Phase 4: Score Storage

```python
def store_scores(session_id: str, scores: SessionScores) -> List[str]:
    """Store all scores to Langfuse."""

    # Get first trace ID for session-level scores
    trace_id = get_first_trace_id(session_id)

    score_ids = []
    for dimension, data in scores.items():
        result = langfuse.create_score(
            trace_id=trace_id,
            name=dimension,
            value=data["score"],
            comment=data.get("rationale", "")
        )
        score_ids.append(result["id"])

    return score_ids
```

### Phase 5: Overall Quality

```python
def calculate_overall_quality(scores: SessionScores) -> float:
    """Weighted average of all dimensions."""

    weights = {
        "context_efficiency": 0.20,
        "instruction_following": 0.25,
        "tool_appropriateness": 0.15,
        "task_completion": 0.25,
        "error_recovery": 0.10,
        "cost_efficiency": 0.05
    }

    # Normalize categorical to 0-1
    categorical_map = {
        "poor": 0.0, "failed": 0.0,
        "partial": 0.33, "slow": 0.33,
        "good": 0.67, "adequate": 0.67, "complete": 0.67,
        "excellent": 1.0, "exceeded": 1.0
    }

    total = 0
    for dim, weight in weights.items():
        score = scores[dim]["score"]
        if isinstance(score, str):
            score = categorical_map.get(score, 0.5)
        total += score * weight

    return total
```

---

## Testing Plan

1. **Unit tests**: Each component in isolation
2. **Integration test**: Score 1 small session end-to-end
3. **Chunking test**: Score 1 large session (100+ traces)
4. **Validation**: Compare AI scores to manual scores from Project 28

---

## Success Criteria

- [ ] SessionScorer class implemented
- [ ] Can score small sessions (<50 traces) in single pass
- [ ] Can score large sessions (100+ traces) with chunking
- [ ] Scores stored correctly to Langfuse
- [ ] Overall quality calculated correctly
- [ ] Tested on 10 sessions with validation

---

## Risks

| Risk | Mitigation |
|------|------------|
| Claude output parsing fails | Strict JSON schema, retry with guidance |
| Chunking loses context | 2-trace overlap, summary in prompt |
| High API cost | Use claude-sonnet-4-5-20250929, batch scoring |
| Score bias | Calibrate against human labels (future project) |

---

## Outputs

- `03-skills/langfuse/langfuse-score-session/` skill with:
  - `scripts/session_scorer.py` - Main scorer class
  - `scripts/session_fetcher.py` - Fetch with observations
  - `scripts/chunk_utils.py` - Chunking logic
  - `scripts/score_storage.py` - Langfuse storage
  - `SKILL.md` - Usage documentation

---

*Ready to execute as Project 29*
