# Project 36: Session Scorer

**Status**: IN_PROGRESS
**Type**: Implementation (Medium)
**Parent Research**: Project 27 - Langfuse Annotation and Scoring Integration
**Dependency**: Project 35 - Score Config Setup (COMPLETE)
**Created**: 2026-01-07
**Updated**: 2026-01-07 (Aligned with Project 35 outputs)

---

## High-Level Goal

Build the core SessionScorer that automatically scores Claude Code sessions across 6 quality dimensions using a Claude subagent, handling large sessions via token-based chunking.

---

## System Context: Self-Improvement Pipeline

```
+-----------------------------------------------------------------------------+
|                    CLAUDE CODE QUALITY MONITORING SYSTEM                     |
+-----------------------------------------------------------------------------+
|                                                                              |
|  PURPOSE: Systematic visibility into session quality with human-reviewed    |
|           suggestions for improvement. NOT autonomous self-improvement.     |
|                                                                              |
|  +--------------+   +--------------+   +--------------+   +--------------+  |
|  |  PROJECT 35  |   |  PROJECT 36  |   |  PROJECT 37  |   |  PROJECT 38  |  |
|  |              |   |              |   |              |   |              |  |
|  |    Score     |-->|   Session    |-->|   Weekly     |-->|   Ground     |  |
|  |   Config     |   |   Scorer     |   |  Monitoring  |   |    Truth     |  |
|  |   Setup      |   |              |   |              |   |  Bootstrap   |  |
|  |              |   |   YOU ARE    |   |              |   |              |  |
|  |  COMPLETE    |   |   HERE       |   |  Synthesizes |   |  Calibrates  |  |
|  |              |   |              |   |  patterns    |   |  AI vs human |  |
|  +--------------+   +--------------+   +--------------+   +--------------+  |
|        |                   |                  |                  |          |
|        v                   v                  v                  v          |
|  +----------------------------------------------------------------------+   |
|  |                         LANGFUSE DATABASE                             |   |
|  |  - Score Configs --------> Scores (attached to traces/sessions)       |   |
|  |  - Sessions/Traces ------> Fetched and analyzed                       |   |
|  |  - Datasets -------------> Ground truth for calibration               |   |
|  +----------------------------------------------------------------------+   |
|                                                                              |
+-----------------------------------------------------------------------------+
```

**Why This Project**: The scorer is the core engine that turns raw session data into quality metrics. Without it, we have no automated scoring capability.

---

## What This Project Does

### Core Capability

```
Input: session_id
Output: 7 scores attached to session's first trace in Langfuse

Process:
1. Fetch session with all traces and observations
2. Extract task context from first user message
3. Build structured session summary (trace timeline)
4. Spawn session-scorer subagent (Sonnet)
5. Parse JSON scores from subagent
6. Calculate overall_quality (weighted aggregate)
7. Store all 7 scores to Langfuse
```

### Deliverables

1. **Session Scorer Skill** (`00-system/skills/meta/langfuse-score-session/`)
   - `SKILL.md` - Orchestration logic and usage
   - `prompts/scorer-prompt.md` - Scoring instructions for subagent

2. **Invocation Pattern** (uses `general-purpose` subagent)
   - Custom `subagent_type` doesn't work (known bug)
   - Subagent reads prompt file, then scores session
   - Returns JSON with scores + evidence + rationales

3. **Test Results**
   - 10 sessions scored with validation
   - Performance metrics (time, cost)

---

## Scoring Dimensions (from Project 35)

| Dimension | Type | Weight | Config ID | What It Measures |
|-----------|------|--------|-----------|------------------|
| goal_achievement | CATEGORICAL | 0.30 | `68cfd90c-8c9e-4907-808d-869ccd9a4c07` | Did it accomplish the goal? |
| tool_efficiency | NUMERIC | 0.20 | `84965473-0f54-4248-999e-7b8627fc9c29` | Right tools used effectively? |
| process_adherence | NUMERIC | 0.20 | `651fc213-4750-4d4e-8155-270235c7cad8` | Proper workflows followed? |
| context_efficiency | NUMERIC | 0.15 | `ae22abed-bd4a-4926-af74-8d71edb1925d` | Context/tokens used efficiently? |
| error_handling | CATEGORICAL | 0.10 | `96c290b7-e3a6-4caa-bace-93cf55f70f1c` | Errors handled well? |
| output_quality | NUMERIC | 0.05 | `d33b1fbf-d3c6-458c-90ca-0b515fe09aed` | Deliverables high quality? |
| overall_quality | NUMERIC | - | `793f09d9-0053-4310-ad32-00dc06c69a71` | Weighted aggregate |

### CATEGORICAL Score Categories

**goal_achievement**:
- `failed` (0): Goal not achieved, abandoned or blocked
- `partial` (1): Some progress but incomplete
- `complete` (2): Goal achieved as requested
- `exceeded` (3): Goal achieved + proactive improvements

**error_handling**:
- `poor` (0): Repeated same failing command
- `struggled` (1): Eventually recovered, many attempts
- `recovered` (2): Quick pivot, good debugging
- `prevented` (3): Proactive checks, clean execution

---

## Architecture: Single Sonnet Scorer

```
+-----------------------------------------------------------------------------+
|                    SINGLE SCORER SUBAGENT ARCHITECTURE                       |
+-----------------------------------------------------------------------------+
|                                                                              |
|  INPUT: session_id                                                          |
|                                                                              |
|  +----------------------------------------------------------------------+   |
|  |  PHASE 1: FETCH & PREPARE (Main Session)                              |   |
|  |                                                                        |   |
|  |  SessionFetcher --> TokenEstimator --> Chunker (if needed)            |   |
|  |        |                                                               |   |
|  |        v                                                               |   |
|  |  SessionSummarizer --> Structured trace timeline                      |   |
|  +----------------------------------------------------------------------+   |
|                                    |                                         |
|                                    v                                         |
|  +----------------------------------------------------------------------+   |
|  |  PHASE 2: SCORE (Subagent via Task tool)                              |   |
|  |                                                                        |   |
|  |  +----------------------------------------------------------------+   |   |
|  |  |                     session-scorer                              |   |   |
|  |  |                       (Sonnet)                                  |   |   |
|  |  |                                                                  |   |   |
|  |  |  Evaluates ALL 6 dimensions in single pass:                     |   |   |
|  |  |                                                                  |   |   |
|  |  |  * goal_achievement   (CATEGORICAL)  weight: 0.30               |   |   |
|  |  |  * tool_efficiency    (NUMERIC)      weight: 0.20               |   |   |
|  |  |  * process_adherence  (NUMERIC)      weight: 0.20               |   |   |
|  |  |  * context_efficiency (NUMERIC)      weight: 0.15               |   |   |
|  |  |  * error_handling     (CATEGORICAL)  weight: 0.10               |   |   |
|  |  |  * output_quality     (NUMERIC)      weight: 0.05               |   |   |
|  |  |                                                                  |   |   |
|  |  |  Returns: JSON with all scores + evidence + rationales          |   |   |
|  |  +----------------------------------------------------------------+   |   |
|  |                                                                        |   |
|  +----------------------------------------------------------------------+   |
|                                    |                                         |
|                                    v                                         |
|  +----------------------------------------------------------------------+   |
|  |  PHASE 3: STORE (Main Session)                                        |   |
|  |                                                                        |   |
|  |  Calculate overall_quality --> Write 7 scores to Langfuse             |   |
|  |                                                                        |   |
|  +----------------------------------------------------------------------+   |
|                                                                              |
+-----------------------------------------------------------------------------+
```

---

## Critical Technical Decisions

### 1. Single Sonnet Scorer (NOT Multi-Critic)

| Aspect | Multi-Critic (rejected) | Single Sonnet (chosen) |
|--------|-------------------------|------------------------|
| Complexity | High (4 subagents) | Low (1 subagent) |
| Context | Duplicated 4x | Single comprehensive view |
| Coherence | Critics may disagree | Holistic evaluation |
| Cost | 4x API calls | 1x API call |
| Quality | Haiku may miss nuance | Sonnet captures nuance |

### 2. Token-Based Chunking (NOT Trace-Count)

**Problem**: Original spec said "20 traces per chunk" but validation showed:
- 20 traces + observations = ~115k tokens = CONTEXT OVERFLOW

**Solution**: Chunk by token budget:
```python
TARGET_TOKENS = 70000   # Leave headroom for prompt + output
MIN_OVERLAP = 4         # Context continuity between chunks
```

### 3. Structured Session Summary (NOT Raw Traces)

Main session prepares structured input for scorer subagent:
- Condensed trace timeline
- Task context from first user message
- Tool usage patterns visible
- Error patterns highlighted

### 4. Observation Fetching Required

**Problem**: `get-session` API returns traces WITHOUT observations

**Solution**: For each trace, call `get-trace` to fetch observation details (costs, actual responses)

---

## Dependencies

**Requires** (SATISFIED):
- Project 35 complete (score configs in Langfuse)
- Langfuse running at localhost:3002
- Anthropic API key for Claude subagent calls

**Enables**:
- Project 37: Weekly Quality Monitoring
- Future specialized critic agents

---

## Success Criteria

- [ ] session-scorer subagent implemented and tested
- [ ] SessionScorer skill implemented
- [ ] Can score small sessions (<50 traces) in single pass
- [ ] Can score large sessions (100+ traces) with chunking
- [ ] Scores stored correctly to Langfuse
- [ ] Overall quality calculated correctly
- [ ] Tested on 10 sessions with validation

---

## Estimated Effort

Medium (3-5 sessions)
- Phase 1: Deep discovery & subagent testing (~1 session)
- Phase 2: Core implementation (~2 sessions)
- Phase 3: Integration & testing (~1-2 sessions)

---

## Reference Materials

In `02-resources/reference/`:
- `enhanced-scoring-design.md` - Full design from P35
- `config-ids.md` - Langfuse config IDs
- `p35-setup-complete.md` - P35 completion report
- `session-size-analysis.md` - Token/chunking analysis
- `trace-structure-analysis.md` - Data model understanding
- `scoring-dimensions.md` - Original dimension definitions

Skill location:
- `00-system/skills/meta/langfuse-score-session/` - Complete skill with prompt

---

*Next: See 02-discovery.md for technical investigation*
