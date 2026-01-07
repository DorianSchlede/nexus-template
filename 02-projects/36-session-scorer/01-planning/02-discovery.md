# Project 36: Discovery

**Date**: 2026-01-07
**Updated**: 2026-01-07 (Aligned with P35 outputs, new subagent architecture)
**Source**: Project 27 research + Project 35 outputs + P34 subagent patterns
**Status**: Discovery complete - ready for execution

---

## Questions & Answers

### Q1: What is the scorer architecture?

**Answer**: Uses `general-purpose` subagent that reads scoring prompt from file.

**NOTE**: Custom `subagent_type` doesn't work (known bug - GitHub Issue #11205). We use `general-purpose` with explicit file read instruction.

```
+-----------------------------------------------------------------------------+
|                 SESSION SCORING WORKFLOW (REVISED)                           |
+-----------------------------------------------------------------------------+
|                                                                              |
|  ORCHESTRATOR (main session)                                                 |
|      │                                                                       |
|      └──► Task(subagent_type="general-purpose",                             |
|             prompt="FIRST: Read 00-system/skills/meta/langfuse-score-session/|
|                     prompts/scorer-prompt.md                                 |
|                     THEN: Score session {id}")                               |
|                                                                              |
|  SUBAGENT (general-purpose with scoring instructions)                       |
|      │                                                                       |
|      ├──► Read scorer-prompt.md for instructions                            |
|      │                                                                       |
|      ├──► Fetch session from Langfuse (list-traces, get-trace)              |
|      │                                                                       |
|      ├──► Analyze traces for evidence                                       |
|      │                                                                       |
|      ├──► Score 6 dimensions                                                |
|      │                                                                       |
|      └──► Return JSON with scores + evidence + rationales                   |
|                                                                              |
|  ORCHESTRATOR                                                                |
|      │                                                                       |
|      ├──► Parse JSON result                                                 |
|      │                                                                       |
|      ├──► Calculate overall_quality (weighted aggregate)                    |
|      │                                                                       |
|      └──► Store 10 scores to Langfuse                                       |
|                                                                              |
+-----------------------------------------------------------------------------+
```

**Key Insight**: The subagent fetches data directly from Langfuse - no pre-summarization needed.

---

### Q2: What are the correct scoring dimensions?

**Answer**: From Project 35 (AUTHORITATIVE):

| Dimension | Type | Weight | Config ID |
|-----------|------|--------|-----------|
| goal_achievement | CATEGORICAL | 0.30 | `68cfd90c-8c9e-4907-808d-869ccd9a4c07` |
| tool_efficiency | NUMERIC | 0.20 | `84965473-0f54-4248-999e-7b8627fc9c29` |
| process_adherence | NUMERIC | 0.20 | `651fc213-4750-4d4e-8155-270235c7cad8` |
| context_efficiency | NUMERIC | 0.15 | `ae22abed-bd4a-4926-af74-8d71edb1925d` |
| error_handling | CATEGORICAL | 0.10 | `96c290b7-e3a6-4caa-bace-93cf55f70f1c` |
| output_quality | NUMERIC | 0.05 | `d33b1fbf-d3c6-458c-90ca-0b515fe09aed` |
| overall_quality | NUMERIC | - | `793f09d9-0053-4310-ad32-00dc06c69a71` |

**CATEGORICAL Categories**:
- **goal_achievement**: failed(0), partial(1), complete(2), exceeded(3)
- **error_handling**: poor(0), struggled(1), recovered(2), prevented(3)

---

### Q3: How does the subagent fetch data?

**Answer**: Using Langfuse skills via Bash:

```bash
# Step 1: Get session metadata
python 03-skills/langfuse/langfuse-get-session/scripts/get_session.py --session-id {session_id}

# Step 2: List all traces in session
python 03-skills/langfuse/langfuse-list-traces/scripts/list_traces.py --session-id {session_id}

# Step 3: For key traces, get full details with observations
python 03-skills/langfuse/langfuse-get-trace/scripts/get_trace.py --trace-id {trace_id}
```

**Critical**: `get-session` does NOT include observations. Must call `get-trace` for each trace.

---

### Q4: What is the subagent input/output contract?

**Answer**: Defined in `00-system/skills/meta/langfuse-score-session/prompts/scorer-prompt.md`

**Input**: Session ID via prompt (after reading prompt file)
```
"FIRST: Read 00-system/skills/meta/langfuse-score-session/prompts/scorer-prompt.md
THEN: Score session {session_id} following those instructions exactly."
```

**Output**: Structured JSON
```json
{
  "session_id": "<session_id>",
  "trace_count": <count>,
  "scores": {
    "goal_achievement": {
      "score": 0-3,
      "label": "failed|partial|complete|exceeded",
      "evidence": ["trace N shows...", "..."],
      "rationale": "1-2 sentences"
    },
    "tool_efficiency": {
      "score": 0.0-1.0,
      "evidence": ["..."],
      "rationale": "..."
    },
    // ... other dimensions
  },
  "metadata": {
    "confidence": 0.0-1.0,
    "notes": "any caveats"
  }
}
```

---

### Q5: How do we handle large sessions?

**Answer**: Subagent sampling strategy:

If session has 50+ traces:
1. Focus on first 10 traces (task context, initial approach)
2. Focus on last 10 traces (completion, final state)
3. Sample every 5th trace in between
4. Note in metadata that sampling was used
5. Adjust confidence based on coverage

Alternative: Token-based chunking with multiple subagent calls (more expensive, deferred).

---

### Q6: How do we invoke the subagent?

**Answer**: Using Claude Code's Task tool with `general-purpose` (custom types don't work):

```python
# Actual invocation (custom subagent_type is broken)
result = Task(
    subagent_type="general-purpose",
    model="sonnet",
    prompt="""
FIRST: Read the scoring instructions from this file:
00-system/skills/meta/langfuse-score-session/prompts/scorer-prompt.md

THEN: Score session {session_id} following those instructions exactly.
Return ONLY the JSON output as specified in the prompt.
"""
)
```

**Key Learning**: Custom `subagent_type` values like `"general-session-scorer"` don't work (GitHub Issue #11205). Only built-in types work: `general-purpose`, `Explore`, `Plan`, `claude-code-guide`.

---

### Q7: How do we store scores to Langfuse?

**Answer**: After parsing subagent JSON, orchestrator stores scores:

```python
# For NUMERIC scores
langfuse.create_score(
    trace_id=first_trace_id,
    name="tool_efficiency",
    value=0.85,
    comment="Good tool selection..."
)

# For CATEGORICAL scores (IMPORTANT!)
langfuse.create_score(
    trace_id=first_trace_id,
    name="goal_achievement",
    value=2,  # Numeric value
    string_value="complete",  # REQUIRED for CATEGORICAL
    comment="Goal achieved..."
)
```

**Key Learnings** (from P35):
- CATEGORICAL scores require BOTH `value` (numeric) AND `stringValue` (label)
- Use `--string-value` argument with langfuse-create-score skill

---

## Components to Build

| Component | Purpose | Complexity | Status |
|-----------|---------|------------|--------|
| `00-system/skills/meta/langfuse-score-session/SKILL.md` | Orchestration logic | Medium | **DONE** |
| `00-system/skills/meta/langfuse-score-session/prompts/scorer-prompt.md` | Scoring instructions | High | **DONE** |
| `scripts/score_session.py` | CLI entry point | Low | TODO |
| `scripts/overall_quality.py` | Weighted aggregate calc | Low | TODO |
| `scripts/score_storage.py` | Store to Langfuse | Low | TODO |

---

## Risk Assessment (Updated)

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Subagent fails to fetch data | Low | High | Clear skill paths in agent definition |
| JSON parsing fails | Medium | Medium | Retry with guidance, strict schema |
| Scoring inconsistency | Medium | Medium | Clear criteria, calibration later |
| Large session overflow | Low | High | Sampling strategy, metadata notes |
| High cost | Low | Low | Single Sonnet call per session |

---

## Reference Materials

**In `02-resources/reference/`**:
- `enhanced-scoring-design.md` - Full design from P35
- `config-ids.md` - Langfuse config IDs
- `p35-setup-complete.md` - P35 completion report
- `session-size-analysis.md` - Token/chunking analysis
- `trace-structure-analysis.md` - Data model

**In `00-system/skills/meta/langfuse-score-session/`**:
- `SKILL.md` - Orchestration and usage
- `prompts/scorer-prompt.md` - Scoring instructions for subagent

**In `02-projects/34-subagent-validation-system/03-working/`**:
- `langfuse-trace-mapping.md` - Subagent trace identification
- `key-insights.md` - Subagent patterns and learnings

---

*Discovery complete. See 03-plan.md for execution strategy.*
