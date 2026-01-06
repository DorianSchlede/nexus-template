# Architecture Design

**Phase**: 6 (Architecture Design)
**Date**: 2026-01-05
**Updated**: 2026-01-05 (Post-Validation Revision)

---

## Overview

This document defines the architecture for a **session quality monitoring system** that:
1. Analyzes Claude Code sessions from Langfuse
2. Scores them across 6 dimensions (revised)
3. Stores scores back to Langfuse
4. Generates improvement suggestions
5. Enables human calibration

**Post-Validation Note**: Rebranded from "self-improvement system" to "quality monitoring system" - the feedback loop for applying suggestions is not yet closed. See validation findings.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SCORING PIPELINE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │   FETCH     │───▶│   SCORE     │───▶│   STORE     │        │
│  │  Sessions   │    │  Sessions   │    │  Scores     │        │
│  └─────────────┘    └─────────────┘    └─────────────┘        │
│        │                  │                  │                 │
│        ▼                  ▼                  ▼                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │  Langfuse   │    │   Claude    │    │  Langfuse   │        │
│  │   API       │    │   Scorer    │    │   Scores    │        │
│  └─────────────┘    └─────────────┘    └─────────────┘        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    IMPROVEMENT LOOP                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │  SYNTHESIZE │───▶│   SUGGEST   │───▶│   APPLY     │        │
│  │  Patterns   │    │ Improvements│    │  Changes    │        │
│  └─────────────┘    └─────────────┘    └─────────────┘        │
│        │                                      │                 │
│        ▼                                      ▼                 │
│  ┌─────────────┐                       ┌─────────────┐        │
│  │  Aggregate  │                       │  System     │        │
│  │  Scores     │                       │  Files      │        │
│  └─────────────┘                       └─────────────┘        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component 1: Session Fetcher

**Purpose**: Retrieve sessions from Langfuse for scoring

### Input
- Date range (default: last 7 days)
- Filter criteria (project, user, min traces)

### Output
- List of session IDs with metadata

### Implementation

```python
def fetch_sessions_for_scoring(
    days_back: int = 7,
    min_traces: int = 3,
    exclude_scored: bool = True
) -> List[SessionInfo]:
    """
    Fetch sessions eligible for scoring.

    Args:
        days_back: How far back to look
        min_traces: Minimum traces to be eligible
        exclude_scored: Skip already-scored sessions

    Returns:
        List of SessionInfo with id, trace_count, created_at
    """
    # 1. List sessions from date range
    sessions = langfuse.list_sessions(
        from_timestamp=datetime.now() - timedelta(days=days_back)
    )

    # 2. Filter by trace count
    sessions = [s for s in sessions if s.trace_count >= min_traces]

    # 3. Optionally exclude already scored
    if exclude_scored:
        sessions = [s for s in sessions if not has_scores(s.id)]

    return sessions
```

### Considerations
- Session trace count not available in list API - need to fetch individually
- May need pagination for large date ranges
- Consider sampling strategy for high volume

---

## Component 2: Session Scorer

**Purpose**: Score a single session across all dimensions

### Design Decision: Single Agent vs Multi-Agent

**Option A: Single General Scorer**
- One Claude call scores all dimensions
- Simpler, fewer API calls
- May miss nuance in specialized areas

**Option B: Specialized Critic Agents**
- Separate agent per dimension
- Better depth per dimension
- More expensive, more complex

**Recommendation: Start with Single Agent**
- Simpler to build and debug
- Can iterate to specialized critics later
- Use structured output for consistency

### Session Scorer Architecture

**Note**: Scoring is done via Claude Code subagents (Task tool), not direct API calls.

```python
class SessionScorer:
    """Score a session across all dimensions."""

    # Updated dimensions after validation
    DIMENSIONS = [
        "task_completion",      # CATEGORICAL - weight 0.30
        "execution_quality",    # NUMERIC - weight 0.25
        "tool_mastery",         # NUMERIC - weight 0.20
        "resource_efficiency",  # NUMERIC - weight 0.15
        "security_compliance",  # CATEGORICAL - weight 0.05
        "user_satisfaction"     # CATEGORICAL - weight 0.05
    ]

    # Token budget for chunking
    TARGET_TOKENS = 70000
    MIN_OVERLAP = 4

    def score_session(self, session_id: str) -> SessionScores:
        # 1. Fetch session with traces
        session = fetch_session_with_traces(session_id)

        # 2. Estimate tokens and check if chunking needed
        estimated_tokens = self.estimate_session_tokens(session)
        if estimated_tokens > 80000:
            return self.score_chunked_session(session)

        # 3. Extract task context (CRITICAL for task_completion scoring)
        task_context = self.extract_task_context(session)

        # 4. Build scoring prompt with task context
        prompt = self.build_scoring_prompt(session, task_context)

        # 5. Score via subagent (Task tool)
        scores = self.score_via_subagent(prompt)

        return scores

    def estimate_session_tokens(self, session: Session) -> int:
        """Estimate total tokens for session (traces + observations)."""
        total = 0
        for trace in session.traces:
            # Trace input tokens (estimate from content length)
            input_chars = len(json.dumps(trace.input or {}))
            total += input_chars // 4

            # Observation tokens (if fetched)
            for obs in trace.observations or []:
                output_chars = len(obs.output or "")
                total += output_chars // 4

        return total

    def extract_task_context(self, session: Session) -> dict:
        """Extract user's original request and objectives."""
        first_user_trace = next(
            (t for t in session.traces if t.metadata.get("messageType") == "user"),
            None
        )

        # Look for TodoWrite objectives
        todo_traces = [t for t in session.traces if "TodoWrite" in str(t.input)]

        return {
            "initial_request": first_user_trace.input if first_user_trace else None,
            "objectives": [t.input for t in todo_traces[:1]]  # First todo list
        }
```

### Scoring Prompt Template

```markdown
# Session Scoring Task

You are scoring a Claude Code session for quality. Analyze the session traces below and score each dimension.

## Session Context
- Session ID: {session_id}
- Traces: {trace_count}
- Project: {project_name}
- Duration: {duration}

## Traces
{formatted_traces}

## Scoring Dimensions

For each dimension, provide:
1. A score (numeric 0-1 or categorical as specified)
2. A brief rationale (1-2 sentences)
3. Key evidence (trace numbers)

### 1. Context Efficiency (0.0-1.0)
How efficiently did the session use context? Were only needed files loaded?

### 2. Instruction Following (poor/partial/good/excellent)
Did the session follow explicit instructions (skills, project steps, user requests)?

### 3. Tool Appropriateness (0.0-1.0)
Were the right tools used for each task?

### 4. Task Completion (failed/partial/complete/exceeded)
Did the session achieve its objective?

### 5. Error Recovery (poor/slow/adequate/excellent)
How well were errors handled and recovered from?

### 6. Cost Efficiency (0.0-1.0)
Was the cost reasonable for the task complexity?

## Output Format

Respond in JSON:
```json
{
  "context_efficiency": {"score": 0.85, "rationale": "...", "evidence": [1, 3, 7]},
  "instruction_following": {"score": "good", "rationale": "...", "evidence": [2, 4]},
  ...
}
```
```

### Chunking Strategy for Large Sessions

**VALIDATED: Token-based chunking required (not trace-count)**

```python
# Configuration
TARGET_TOKENS = 70000   # Leave headroom for prompt + output
MIN_OVERLAP = 4         # Traces for context continuity (validated: 2 is insufficient)
MIN_CHUNK_RATIO = 0.5   # Minimum chunk size vs previous

def chunk_by_tokens(traces: List[Trace], target: int = TARGET_TOKENS, overlap: int = MIN_OVERLAP) -> List[List[Trace]]:
    """Split session into chunks based on TOKEN budget, not trace count.

    Key insight from validation: 20 traces + observations = ~115k tokens,
    which OVERFLOWS 100k context. Must use dynamic token-based chunking.
    """
    chunks = []
    current = []
    current_tokens = 0

    for trace in traces:
        trace_tokens = estimate_trace_tokens(trace)

        # Check if adding this trace exceeds budget
        if current_tokens + trace_tokens > target and len(current) > overlap:
            chunks.append(current)
            # Keep overlap traces for context continuity
            current = current[-overlap:]
            current_tokens = sum(estimate_trace_tokens(t) for t in current)

        current.append(trace)
        current_tokens += trace_tokens

    # Handle final chunk
    if current:
        if chunks and len(current) < len(chunks[-1]) * MIN_CHUNK_RATIO:
            # Merge small final chunk with previous
            chunks[-1].extend(current[overlap:])
        else:
            chunks.append(current)

    return chunks

def estimate_trace_tokens(trace: Trace) -> int:
    """Estimate tokens for a single trace including observations."""
    tokens = 0

    # Input tokens (from content length)
    input_content = json.dumps(trace.input or {})
    tokens += len(input_content) // 4

    # Observation tokens
    for obs in trace.observations or []:
        tokens += len(obs.output or "") // 4
        tokens += 200  # Overhead for observation metadata

    return tokens

def aggregate_chunk_scores(chunk_scores: List[ChunkScores]) -> SessionScores:
    """Combine chunk scores into session scores.

    VALIDATED: Report variance for transparency.
    """
    aggregated = {}

    # Numeric dimensions: weighted average + variance
    for dim in ["execution_quality", "tool_mastery", "resource_efficiency"]:
        scores = [c[dim]["score"] for c in chunk_scores]
        aggregated[dim] = {
            "score": sum(scores) / len(scores),
            "min": min(scores),
            "max": max(scores),
            "variance": statistics.variance(scores) if len(scores) > 1 else 0,
            "chunk_scores": scores
        }

    # Categorical dimensions: confidence-weighted voting
    for dim in ["task_completion", "security_compliance", "user_satisfaction"]:
        scores = [c[dim]["score"] for c in chunk_scores]
        vote_result = confidence_weighted_vote(scores)
        aggregated[dim] = {
            "score": vote_result["winner"],
            "confidence": vote_result["confidence"],
            "chunk_scores": scores,
            "tie_flag": vote_result.get("tie", False)
        }

    return aggregated

def confidence_weighted_vote(scores: List[str]) -> dict:
    """Majority vote with tie handling and confidence."""
    from collections import Counter
    counts = Counter(scores)
    total = len(scores)

    if len(counts) == 0:
        return {"winner": "neutral", "confidence": 0}

    top_two = counts.most_common(2)
    winner = top_two[0][0]
    winner_count = top_two[0][1]

    # Check for tie
    if len(top_two) > 1 and top_two[0][1] == top_two[1][1]:
        return {
            "winner": winner,
            "confidence": winner_count / total,
            "tie": True,
            "tied_with": top_two[1][0]
        }

    return {
        "winner": winner,
        "confidence": winner_count / total
    }
```

---

## Component 3: Score Storage

**Purpose**: Persist scores to Langfuse

### Score Config Setup

Create these score configs once (via skill or script):

```python
SCORE_CONFIGS = [
    {
        "name": "context_efficiency",
        "dataType": "NUMERIC",
        "minValue": 0,
        "maxValue": 1,
        "description": "How efficiently context was used"
    },
    {
        "name": "instruction_following",
        "dataType": "CATEGORICAL",
        "categories": ["poor", "partial", "good", "excellent"],
        "description": "How well instructions were followed"
    },
    {
        "name": "tool_appropriateness",
        "dataType": "NUMERIC",
        "minValue": 0,
        "maxValue": 1,
        "description": "Appropriateness of tool choices"
    },
    {
        "name": "task_completion",
        "dataType": "CATEGORICAL",
        "categories": ["failed", "partial", "complete", "exceeded"],
        "description": "Whether the task was completed"
    },
    {
        "name": "error_recovery",
        "dataType": "CATEGORICAL",
        "categories": ["poor", "slow", "adequate", "excellent"],
        "description": "Quality of error handling"
    },
    {
        "name": "cost_efficiency",
        "dataType": "NUMERIC",
        "minValue": 0,
        "maxValue": 1,
        "description": "Cost relative to task complexity"
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

### Score Storage Implementation

```python
def store_session_scores(
    session_id: str,
    scores: SessionScores,
    trace_id: str = None  # Optional: score at trace level
) -> List[str]:
    """Store scores to Langfuse."""

    score_ids = []

    for dimension, data in scores.items():
        # Convert categorical to numeric for API
        if isinstance(data["score"], str):
            value = categorical_to_numeric(dimension, data["score"])
        else:
            value = data["score"]

        # Create score
        result = langfuse.create_score(
            trace_id=trace_id or get_first_trace(session_id),
            name=dimension,
            value=value,
            comment=data.get("rationale", ""),
            config_id=get_config_id(dimension)
        )
        score_ids.append(result["id"])

    # Store overall quality
    overall = calculate_overall_quality(scores)
    result = langfuse.create_score(
        trace_id=trace_id or get_first_trace(session_id),
        name="overall_quality",
        value=overall,
        comment="Weighted aggregate score"
    )
    score_ids.append(result["id"])

    return score_ids
```

---

## Component 4: Pattern Synthesizer

**Purpose**: Aggregate scores and identify patterns

### Weekly Synthesis

```python
def synthesize_weekly_patterns(
    from_date: datetime,
    to_date: datetime
) -> SynthesisReport:
    """Analyze scored sessions for patterns."""

    # 1. Fetch all scores in date range
    scores = fetch_scores_in_range(from_date, to_date)

    # 2. Calculate dimension averages
    dimension_stats = {}
    for dim in DIMENSIONS:
        values = [s[dim]["score"] for s in scores]
        dimension_stats[dim] = {
            "mean": statistics.mean(values),
            "stdev": statistics.stdev(values),
            "min": min(values),
            "max": max(values),
            "trend": calculate_trend(values)  # vs previous week
        }

    # 3. Identify outliers
    outliers = {
        "excellent": [s for s in scores if s["overall"] > 0.85],
        "poor": [s for s in scores if s["overall"] < 0.5]
    }

    # 4. Extract common issues
    issues = extract_common_issues(
        [s for s in scores if s["overall"] < 0.7]
    )

    return SynthesisReport(
        date_range=(from_date, to_date),
        sessions_scored=len(scores),
        dimension_stats=dimension_stats,
        outliers=outliers,
        common_issues=issues
    )
```

---

## Component 5: Improvement Suggester

**Purpose**: Generate actionable improvement suggestions

### Suggestion Generation

```python
def generate_improvement_suggestions(
    synthesis: SynthesisReport
) -> List[ImprovementSuggestion]:
    """Generate suggestions from synthesis report."""

    suggestions = []

    # Check each dimension for issues
    for dim, stats in synthesis.dimension_stats.items():
        if stats["mean"] < 0.7:
            # This dimension needs improvement
            suggestion = generate_dimension_suggestion(dim, stats)
            suggestions.append(suggestion)

    # Check for systemic issues
    if synthesis.common_issues:
        for issue in synthesis.common_issues[:3]:  # Top 3
            suggestion = generate_issue_suggestion(issue)
            suggestions.append(suggestion)

    return suggestions

def generate_dimension_suggestion(
    dimension: str,
    stats: DimensionStats
) -> ImprovementSuggestion:
    """Generate suggestion for underperforming dimension."""

    # Use Claude to generate actionable suggestion
    prompt = f"""
    The dimension "{dimension}" is underperforming:
    - Mean score: {stats['mean']:.2f}
    - Trend: {stats['trend']}

    Based on the scoring criteria for this dimension, suggest:
    1. What system changes could improve this?
    2. What patterns should be added to CLAUDE.md?
    3. What skills might need updating?

    Be specific and actionable.
    """

    response = claude.generate(prompt)

    return ImprovementSuggestion(
        dimension=dimension,
        severity="high" if stats["mean"] < 0.5 else "medium",
        suggestion=response,
        evidence=stats
    )
```

---

## Component 6: Human Calibration

**Purpose**: Enable human review and calibration of AI scores

### Ground Truth Dataset

```python
def create_ground_truth_item(
    session_id: str,
    human_scores: Dict[str, Any]
) -> str:
    """Add human-labeled session to ground truth dataset."""

    return langfuse.create_dataset_item(
        dataset_name="self-improvement-ground-truth",
        input={
            "session_id": session_id,
            "session_data": fetch_session_summary(session_id)
        },
        expected_output=human_scores,
        metadata={
            "labeled_by": "human",
            "labeled_at": datetime.now().isoformat()
        }
    )
```

### Calibration Workflow

```
1. AI scores session
   └── Scores stored to Langfuse

2. Human reviews sample of AI scores
   └── Via Langfuse UI or custom interface

3. Human provides corrections
   └── Added to ground truth dataset

4. Compare AI vs human scores
   └── Calculate agreement metrics

5. If disagreement > threshold
   └── Adjust scoring prompts
   └── Re-score affected sessions
```

### Agreement Metrics

```python
def calculate_calibration_metrics(
    ai_scores: List[SessionScores],
    human_scores: List[SessionScores]
) -> CalibrationMetrics:
    """Compare AI and human scores."""

    metrics = {}

    for dim in DIMENSIONS:
        ai = [s[dim]["score"] for s in ai_scores]
        human = [s[dim]["score"] for s in human_scores]

        if dim in NUMERIC_DIMENSIONS:
            metrics[dim] = {
                "correlation": scipy.stats.pearsonr(ai, human),
                "mae": mean_absolute_error(ai, human),
                "bias": np.mean(ai) - np.mean(human)
            }
        else:
            metrics[dim] = {
                "agreement": cohen_kappa_score(ai, human),
                "confusion_matrix": confusion_matrix(ai, human)
            }

    return CalibrationMetrics(metrics)
```

---

## Execution Schedule

### Weekly Scoring Run

```
SCHEDULE: Every Sunday at 2am

1. FETCH
   - Get sessions from past 7 days
   - Filter: min 3 traces, not already scored
   - Expected: 20-50 sessions

2. SCORE
   - Process each session
   - Chunk if >50 traces
   - Store scores to Langfuse

3. SYNTHESIZE
   - Calculate dimension averages
   - Identify outliers
   - Extract common issues

4. SUGGEST
   - Generate improvement suggestions
   - Save to 01-memory/core-learnings.md
   - Create improvement task if significant

5. REPORT
   - Generate weekly summary
   - Save to 01-memory/session-reports/
```

---

## Implementation Phases

### Phase A: Score Config Setup (Project 28)
- Create all score configs in Langfuse
- Create ground truth dataset
- Test scoring on 5 sessions manually

### Phase B: Session Scorer (Project 29)
- Build SessionScorer class
- Implement chunking strategy
- Test on 20 sessions

### Phase C: Weekly Workflow (Project 30)
- Build fetcher, scorer, synthesizer
- Create scheduled skill
- Run first full cycle

### Phase D: Human Calibration (Project 31)
- Label 50 sessions manually
- Calculate calibration metrics
- Adjust scoring prompts

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Scorer bias | Calibrate against human labels |
| High API cost | Batch scoring, use efficient model |
| Context overflow | Chunking strategy in place |
| Score drift | Weekly human review sample |
| Annotation queues fail | Use datasets API instead |

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Sessions scored per week | 20+ |
| Human-AI score correlation | >0.8 |
| Improvement suggestions implemented | 2+ per month |
| Overall quality trend | +0.05 per month |

---

*Next: Phase 7 - Research Outputs & Spawned Projects*
