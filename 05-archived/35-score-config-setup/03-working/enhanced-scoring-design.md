# Enhanced Scoring System Design

**Date**: 2026-01-07
**Status**: DESIGN PHASE
**Updated**: 2026-01-07 (Single Sonnet scorer architecture)
**Supersedes**: Original 7-dimension design from Project 27

---

## Architecture: Single Sonnet Scorer Subagent

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SINGLE SCORER SUBAGENT ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  INPUT: session_id                                                          │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  PHASE 1: FETCH & PREPARE (Main Session)                              │   │
│  │                                                                        │   │
│  │  SessionFetcher → TokenEstimator → Chunker (if needed) → Summarizer  │   │
│  │                                                                        │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  PHASE 2: SCORE (Single Sonnet Subagent via Task tool)                │   │
│  │                                                                        │   │
│  │  ┌────────────────────────────────────────────────────────────────┐  │   │
│  │  │                     SESSION SCORER                              │  │   │
│  │  │                       (Sonnet)                                  │  │   │
│  │  │                                                                  │  │   │
│  │  │  Evaluates ALL 6 dimensions in single pass:                     │  │   │
│  │  │                                                                  │  │   │
│  │  │  • goal_achievement   (CATEGORICAL)  weight: 0.30               │  │   │
│  │  │  • tool_efficiency    (NUMERIC)      weight: 0.20               │  │   │
│  │  │  • process_adherence  (NUMERIC)      weight: 0.20               │  │   │
│  │  │  • context_efficiency (NUMERIC)      weight: 0.15               │  │   │
│  │  │  • error_handling     (CATEGORICAL)  weight: 0.10               │  │   │
│  │  │  • output_quality     (NUMERIC)      weight: 0.05               │  │   │
│  │  │                                                                  │  │   │
│  │  │  Returns: JSON with all scores + evidence + rationales          │  │   │
│  │  └────────────────────────────────────────────────────────────────┘  │   │
│  │                                                                        │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  PHASE 3: STORE (Main Session)                                        │   │
│  │                                                                        │   │
│  │  Calculate overall_quality → Write 7 scores to Langfuse               │   │
│  │                                                                        │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│                          LANGFUSE: 7 scores on trace                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Why Single Sonnet Scorer?

| Aspect | Multi-Critic | Single Sonnet |
|--------|--------------|---------------|
| Complexity | High (4 subagents) | Low (1 subagent) |
| Context | Duplicated across critics | Single comprehensive view |
| Coherence | May disagree across critics | Holistic evaluation |
| Cost | 4x API calls | 1x API call |
| Orchestration | Complex parallel spawning | Simple single spawn |
| Quality | Haiku may miss nuance | Sonnet captures nuance |

**Decision**: Single Sonnet scorer is simpler, cheaper, and provides more coherent evaluation since one agent sees the full picture.

---

## Enhanced Scoring Dimensions

### Design Principles

1. **Measurable**: Each dimension has observable evidence in traces
2. **Actionable**: Low scores point to specific improvements
3. **Nexus-Aware**: Dimensions reflect Nexus system patterns
4. **Non-Overlapping**: Each dimension measures something distinct

---

### Dimension 1: Goal Achievement

**Name**: `goal_achievement`
**Type**: CATEGORICAL
**Categories**: `failed` (0), `partial` (1), `complete` (2), `exceeded` (3)
**Weight**: 0.30

**What It Measures**: Did the session accomplish what the user asked for?

**Evidence to Look For**:
- First user message → defines the goal
- Final state → matches requested outcome?
- Explicit completion signals ("done", "thanks", commit created)
- Deliverables created (files written, tests passing)

**Scoring Criteria**:
| Score | Criteria |
|-------|----------|
| failed | Goal not achieved, session abandoned or blocked |
| partial | Some progress but incomplete delivery |
| complete | Goal achieved as requested |
| exceeded | Goal achieved + proactive improvements |

---

### Dimension 2: Tool Efficiency

**Name**: `tool_efficiency`
**Type**: NUMERIC (0.0 - 1.0)
**Weight**: 0.20

**What It Measures**: Did the session use the right tools effectively?

**Evidence to Look For**:
- Tool selection patterns (Read vs cat, Edit vs sed, Grep vs grep)
- Retry counts (same tool called multiple times with errors)
- Parallel vs sequential tool calls
- Task tool for exploration vs raw Bash

**Scoring Criteria**:
| Score | Criteria |
|-------|----------|
| 0.0-0.3 | Wrong tools, many retries, Bash for file ops |
| 0.4-0.6 | Some misuse, moderate retries |
| 0.7-0.8 | Generally correct, few retries |
| 0.9-1.0 | Optimal tool selection, parallel where possible |

---

### Dimension 3: Process Adherence

**Name**: `process_adherence`
**Type**: NUMERIC (0.0 - 1.0)
**Weight**: 0.20

**What It Measures**: Did the session follow proper workflows?

**Evidence to Look For**:
- TodoWrite usage for multi-step tasks
- Read before Edit pattern
- Skill loading via proper patterns
- Project workflow compliance (execute-project steps)

**Scoring Criteria**:
| Score | Criteria |
|-------|----------|
| 0.0-0.3 | Ignored workflows, no planning, chaotic execution |
| 0.4-0.6 | Some process followed, gaps in discipline |
| 0.7-0.8 | Good process adherence, minor deviations |
| 0.9-1.0 | Exemplary workflow execution, proper patterns |

---

### Dimension 4: Context Efficiency

**Name**: `context_efficiency`
**Type**: NUMERIC (0.0 - 1.0)
**Weight**: 0.15

**What It Measures**: How efficiently was context/tokens used?

**Evidence to Look For**:
- Files read vs files actually used in task
- Repeated reads of same file
- Full file reads vs targeted reads (offset/limit)
- Task tool for exploration vs bloating main context

**Scoring Criteria**:
| Score | Criteria |
|-------|----------|
| 0.0-0.3 | Excessive file loading, many re-reads, bloated context |
| 0.4-0.6 | Some redundancy, moderate inefficiency |
| 0.7-0.8 | Reasonable context usage, minor waste |
| 0.9-1.0 | Minimal context, targeted reads, good delegation |

---

### Dimension 5: Error Handling

**Name**: `error_handling`
**Type**: CATEGORICAL
**Categories**: `poor` (0), `struggled` (1), `recovered` (2), `prevented` (3)
**Weight**: 0.10

**What It Measures**: How were errors and blockers handled?

**Evidence to Look For**:
- Tool errors and response patterns
- Pivot strategies after failures
- Proactive error prevention (checks before actions)
- Escalation to user when appropriate

**Scoring Criteria**:
| Score | Criteria |
|-------|----------|
| poor | Repeated same failing command, ignored errors |
| struggled | Eventually recovered but took many attempts |
| recovered | Quick pivot on errors, good debugging |
| prevented | Proactive checks prevented errors, clean execution |

---

### Dimension 6: Output Quality

**Name**: `output_quality`
**Type**: NUMERIC (0.0 - 1.0)
**Weight**: 0.05

**What It Measures**: Quality of the actual deliverables produced.

**Evidence to Look For**:
- Code compiles/runs (if applicable)
- Tests pass (if modified)
- Markdown formatting correct
- File references use proper links (VSCode)
- No unnecessary emojis (unless requested)

**Scoring Criteria**:
| Score | Criteria |
|-------|----------|
| 0.0-0.3 | Broken output, syntax errors, poor formatting |
| 0.4-0.6 | Functional but rough, minor issues |
| 0.7-0.8 | Good quality, clean output |
| 0.9-1.0 | Excellent quality, polished deliverables |

---

### Aggregate: Overall Quality

**Name**: `overall_quality`
**Type**: NUMERIC (0.0 - 1.0)

**Formula**:
```python
# Normalize categorical to 0-1 (0→0.0, 1→0.33, 2→0.67, 3→1.0)
def normalize_categorical(value: int) -> float:
    return value / 3.0

overall = (
    normalize_categorical(goal_achievement) * 0.30 +
    tool_efficiency * 0.20 +
    process_adherence * 0.20 +
    context_efficiency * 0.15 +
    normalize_categorical(error_handling) * 0.10 +
    output_quality * 0.05
)
```

---

## Score Config Specifications (for Langfuse)

```python
SCORE_CONFIGS = [
    # CATEGORICAL dimensions
    {
        "name": "goal_achievement",
        "dataType": "CATEGORICAL",
        "categories": [
            {"label": "failed", "value": 0},
            {"label": "partial", "value": 1},
            {"label": "complete", "value": 2},
            {"label": "exceeded", "value": 3}
        ],
        "description": "Did the session accomplish the user's goal?"
    },
    {
        "name": "error_handling",
        "dataType": "CATEGORICAL",
        "categories": [
            {"label": "poor", "value": 0},
            {"label": "struggled", "value": 1},
            {"label": "recovered", "value": 2},
            {"label": "prevented", "value": 3}
        ],
        "description": "How were errors and blockers handled?"
    },

    # NUMERIC dimensions
    {
        "name": "tool_efficiency",
        "dataType": "NUMERIC",
        "minValue": 0,
        "maxValue": 1,
        "description": "Right tool selection and usage efficiency"
    },
    {
        "name": "process_adherence",
        "dataType": "NUMERIC",
        "minValue": 0,
        "maxValue": 1,
        "description": "Following proper workflows (TodoWrite, Read→Edit, skills)"
    },
    {
        "name": "context_efficiency",
        "dataType": "NUMERIC",
        "minValue": 0,
        "maxValue": 1,
        "description": "Efficient use of context window and file reads"
    },
    {
        "name": "output_quality",
        "dataType": "NUMERIC",
        "minValue": 0,
        "maxValue": 1,
        "description": "Quality of deliverables (code, docs, formatting)"
    },
    {
        "name": "overall_quality",
        "dataType": "NUMERIC",
        "minValue": 0,
        "maxValue": 1,
        "description": "Weighted aggregate of all dimensions"
    }
]
```

---

## Single Scorer Subagent Workflow

### Step 1: Main Session Fetches & Prepares Data

```python
# Fetch session with all traces and observations
session = langfuse.get_session(session_id)
traces = []
for t in session.traces:
    trace = langfuse.get_trace(t.id)
    traces.append(trace)

# Check token budget, chunk if needed
total_tokens = estimate_session_tokens(traces)
if total_tokens > 80000:
    chunks = chunk_by_tokens(traces, target=70000)
else:
    chunks = [traces]  # Single chunk

# Prepare session summary for scorer
session_summary = summarize_session(traces)
task_context = extract_task_context(traces)  # First user message
```

### Step 2: Spawn Single Sonnet Scorer Subagent

```python
# Single Task tool call with comprehensive prompt
scorer_result = Task(
    subagent_type="session-scorer",
    model="sonnet",
    prompt=SCORER_PROMPT.format(
        session_id=session_id,
        session_summary=session_summary,
        task_context=task_context,
        trace_count=len(traces),
    )
)
```

### Step 3: Parse Results & Store to Langfuse

```python
# Parse JSON response from scorer
scores = json.loads(scorer_result)

# Calculate overall_quality
scores["overall_quality"] = calculate_overall_quality(scores)

# Write all 7 scores to Langfuse
for dimension, data in scores.items():
    langfuse.create_score(
        trace_id=first_trace_id,
        name=dimension,
        value=data["score"],
        comment=data["rationale"],
        config_id=config_ids[dimension]
    )
```

---

## Scorer Prompt Template

```markdown
# Session Quality Scorer

You are a quality scorer for Claude Code sessions. Analyze the session below and score it across 6 dimensions.

## Session Information

- **Session ID**: {session_id}
- **Trace Count**: {trace_count}
- **Task Context** (what the user asked for):
{task_context}

## Session Summary

{session_summary}

## Scoring Dimensions

Score each dimension based on the evidence in the session:

### 1. Goal Achievement (CATEGORICAL)
Did the session accomplish the user's goal?
- **failed** (0): Goal not achieved, abandoned or blocked
- **partial** (1): Some progress but incomplete
- **complete** (2): Goal achieved as requested
- **exceeded** (3): Goal achieved + proactive improvements

### 2. Tool Efficiency (NUMERIC 0.0-1.0)
Were the right tools used effectively?
- Check: Read vs cat, Edit vs sed, Grep vs grep
- Check: Parallel calls when independent
- Check: Task tool for exploration
- 0.0-0.3 = Wrong tools, many retries
- 0.7-1.0 = Optimal selection, parallel where possible

### 3. Process Adherence (NUMERIC 0.0-1.0)
Were proper workflows followed?
- Check: TodoWrite for multi-step tasks
- Check: Read before Edit pattern
- Check: Proper skill loading (not Bash)
- 0.0-0.3 = Ignored workflows, chaotic
- 0.7-1.0 = Exemplary process

### 4. Context Efficiency (NUMERIC 0.0-1.0)
Was context used efficiently?
- Check: Files read vs files used ratio
- Check: Repeated reads of same file
- Check: Task tool for exploration (not bloating main)
- 0.0-0.3 = Excessive loading, many re-reads
- 0.7-1.0 = Minimal context, targeted reads

### 5. Error Handling (CATEGORICAL)
How were errors handled?
- **poor** (0): Repeated same failing command
- **struggled** (1): Eventually recovered, many attempts
- **recovered** (2): Quick pivot, good debugging
- **prevented** (3): Proactive checks, clean execution

### 6. Output Quality (NUMERIC 0.0-1.0)
Quality of deliverables?
- Check: Code compiles/runs
- Check: Proper formatting
- Check: Concise responses
- 0.0-0.3 = Broken, syntax errors
- 0.7-1.0 = Excellent, polished

## Output Format

Return ONLY valid JSON:

```json
{
  "goal_achievement": {
    "score": 0-3,
    "evidence": ["trace X shows...", "trace Y shows..."],
    "rationale": "1-2 sentence explanation"
  },
  "tool_efficiency": {
    "score": 0.0-1.0,
    "evidence": ["used Read correctly", "parallel calls"],
    "rationale": "1-2 sentence explanation"
  },
  "process_adherence": {
    "score": 0.0-1.0,
    "evidence": ["TodoWrite used", "Read before Edit"],
    "rationale": "1-2 sentence explanation"
  },
  "context_efficiency": {
    "score": 0.0-1.0,
    "evidence": ["minimal re-reads", "used Task for exploration"],
    "rationale": "1-2 sentence explanation"
  },
  "error_handling": {
    "score": 0-3,
    "evidence": ["quick recovery from X error"],
    "rationale": "1-2 sentence explanation"
  },
  "output_quality": {
    "score": 0.0-1.0,
    "evidence": ["code compiles", "clean formatting"],
    "rationale": "1-2 sentence explanation"
  }
}
```
```

---

## Chunking for Large Sessions

For sessions exceeding 80k tokens:

```python
def score_chunked_session(session_id: str, chunks: List[List[Trace]]) -> dict:
    """Score large session by chunks, then aggregate."""

    chunk_scores = []
    for i, chunk in enumerate(chunks):
        chunk_summary = summarize_chunk(chunk, is_first=(i==0), is_last=(i==len(chunks)-1))

        # Score this chunk
        result = Task(
            subagent_type="session-scorer",
            model="sonnet",
            prompt=CHUNK_SCORER_PROMPT.format(
                chunk_number=i+1,
                total_chunks=len(chunks),
                chunk_summary=chunk_summary,
                task_context=task_context if i==0 else "See chunk 1",
            )
        )
        chunk_scores.append(json.loads(result))

    # Aggregate chunk scores
    return aggregate_chunk_scores(chunk_scores)

def aggregate_chunk_scores(chunk_scores: List[dict]) -> dict:
    """Combine scores from multiple chunks."""
    aggregated = {}

    # NUMERIC: weighted average
    for dim in ["tool_efficiency", "process_adherence", "context_efficiency", "output_quality"]:
        values = [c[dim]["score"] for c in chunk_scores]
        aggregated[dim] = {
            "score": sum(values) / len(values),
            "rationale": f"Average across {len(values)} chunks",
            "chunk_scores": values
        }

    # CATEGORICAL: take from final chunk (has full context)
    for dim in ["goal_achievement", "error_handling"]:
        aggregated[dim] = chunk_scores[-1][dim]  # Last chunk has completion info

    return aggregated
```

---

## Comparison: Old vs New

| Aspect | Old Design (P27) | New Design |
|--------|------------------|------------|
| Dimensions | 7 generic | 6 specific + 1 aggregate |
| Measurability | Low (all judgment) | High (partial auto-signals) |
| Scorer | Undefined | Single Sonnet subagent |
| Nexus-aware | No | Yes (process_adherence) |
| Architecture | Complex multi-critic | Simple single scorer |
| Model | Mixed | Sonnet only |
| Cost | 4x (multi-critic) | 1x (single) |

---

## Migration Path

### Phase 1: Create New Configs (Project 35)
- Create 7 score configs with enhanced dimensions
- Test on sample trace

### Phase 2: Build Scorer (Project 36)
- Implement single Sonnet scorer subagent
- Build session fetcher and summarizer
- Implement chunking for large sessions
- Test on diverse sessions

### Phase 3: Calibrate
- Score 20 sessions
- Compare AI scores to human judgment
- Adjust prompt/criteria as needed

---

*Ready for implementation. See 04-steps.md for execution tasks.*
