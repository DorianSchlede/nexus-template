# Project 36: Execution Plan

**Date**: 2026-01-07
**Updated**: 2026-01-07 (Revised architecture - subagent fetches directly)
**Status**: READY FOR EXECUTION (P35 complete)

---

## Strategy

Execute in 3 phases:
1. **Phase 1: Subagent Testing** - Validate scorer via general-purpose subagent
2. **Phase 2: Orchestrator Implementation** - Build skill to invoke and process results
3. **Phase 3: Validation** - Test on diverse sessions, measure performance

**Architecture**: Uses `general-purpose` subagent with prompt file (`00-system/skills/meta/langfuse-score-session/prompts/scorer-prompt.md`) to fetch data from Langfuse and score all 6 dimensions in one pass.

**NOTE**: Custom `subagent_type` doesn't work (GitHub Issue #11205). We use `general-purpose` with explicit file read instruction.

---

## Architecture: Subagent-Driven Scoring

```
+-----------------------------------------------------------------------------+
|                    SUBAGENT-DRIVEN SCORING ARCHITECTURE                      |
+-----------------------------------------------------------------------------+
|                                                                              |
|  ORCHESTRATOR SKILL (00-system/skills/meta/langfuse-score-session/)         |
|      │                                                                       |
|      └──► Task(subagent_type="general-purpose",                             |
|             prompt="FIRST: Read prompts/scorer-prompt.md                     |
|                     THEN: Score session {id}")                               |
|                                                                              |
|  +-----------------------------------------------------------------------+  |
|  |  SUBAGENT: general-purpose (with scoring instructions from prompt)     |  |
|  |                                                                         |  |
|  |  1. Read scorer-prompt.md for instructions                             |  |
|  |  2. Fetch session from Langfuse                                        |  |
|  |     - get-session → metadata                                           |  |
|  |     - list-traces → all traces                                         |  |
|  |     - get-trace → observations (for key traces)                        |  |
|  |  3. Analyze traces for evidence                                        |  |
|  |  4. Score 6 dimensions:                                                |  |
|  |     - goal_achievement (CATEGORICAL 0-3)                               |  |
|  |     - tool_efficiency (NUMERIC 0-1)                                    |  |
|  |     - process_adherence (NUMERIC 0-1)                                  |  |
|  |     - context_efficiency (NUMERIC 0-1)                                 |  |
|  |     - error_handling (CATEGORICAL 0-3)                                 |  |
|  |     - output_quality (NUMERIC 0-1)                                     |  |
|  |  5. Return JSON result                                                 |  |
|  +-----------------------------------------------------------------------+  |
|                                    │                                         |
|                                    ▼                                         |
|  ORCHESTRATOR POST-PROCESSING                                               |
|      │                                                                       |
|      ├──► Parse JSON from subagent                                          |
|      │                                                                       |
|      ├──► Calculate overall_quality (weighted aggregate)                    |
|      │    formula: 0.30*goal + 0.20*tool + 0.20*process +                   |
|      │             0.15*context + 0.10*error + 0.05*output                  |
|      │                                                                       |
|      └──► Store 7 scores to Langfuse                                        |
|           - 4 NUMERIC: tool, process, context, output                       |
|           - 2 CATEGORICAL: goal, error (with string_value!)                 |
|           - 1 AGGREGATE: overall_quality                                    |
|                                                                              |
+-----------------------------------------------------------------------------+
```

---

## Why Subagent Fetches Directly?

| Aspect | Pre-Summarized Input (rejected) | Subagent Fetches (chosen) |
|--------|--------------------------------|---------------------------|
| Context | Main session must summarize | Subagent sees raw data |
| Flexibility | Rigid summary format | Subagent decides what to read |
| Tool access | None | Full Langfuse skills |
| Accuracy | Depends on summarizer | Subagent verifies |
| Complexity | Complex orchestrator | Simple orchestrator |

**Decision**: Let the subagent fetch directly - it's smarter and can decide what evidence it needs.

---

## Phase 1: Subagent Testing (1 session)

### Goals
- Validate scoring via general-purpose subagent works
- Test Langfuse skill invocation from subagent
- Verify JSON output format

### Tasks
1. Pick a small session (5-10 traces) from Langfuse
2. Manually invoke subagent via Task tool
3. Verify it fetches data correctly
4. Verify JSON output matches schema
5. Document any issues in `03-working/subagent-testing.md`

### Test Script (Actual)
```python
# In main session - use general-purpose with prompt file read
result = Task(
    subagent_type="general-purpose",
    model="sonnet",
    prompt="""
FIRST: Read the scoring instructions from this file:
00-system/skills/meta/langfuse-score-session/prompts/scorer-prompt.md

THEN: Score session abc123 following those instructions exactly.
Return ONLY the JSON output as specified in the prompt.
"""
)
print(result)  # Should be valid JSON
```

---

## Phase 2: Orchestrator Implementation (1-2 sessions)

### Goals
- Build the langfuse-score-session skill
- Implement overall_quality calculation
- Implement score storage to Langfuse

### Components

#### 2.1 Score Session CLI (`scripts/score_session.py`)
```python
#!/usr/bin/env python3
"""CLI to score a session using the general-purpose subagent with scoring prompt."""

import argparse
import json
import sys

# This script is invoked by the main session AFTER the subagent returns
# It handles:
# 1. Parsing the JSON result
# 2. Calculating overall_quality
# 3. Storing all 7 scores to Langfuse

def calculate_overall_quality(scores: dict) -> float:
    """Weighted aggregate with categorical normalization."""
    def normalize_cat(value: int) -> float:
        return value / 3.0

    weights = {
        "goal_achievement": 0.30,
        "tool_efficiency": 0.20,
        "process_adherence": 0.20,
        "context_efficiency": 0.15,
        "error_handling": 0.10,
        "output_quality": 0.05,
    }

    total = 0
    for dim, weight in weights.items():
        score_data = scores.get(dim, {})
        value = score_data.get("score", 0)
        if dim in ["goal_achievement", "error_handling"]:
            value = normalize_cat(value)
        total += value * weight

    return round(total, 3)

def store_scores(session_id: str, scores: dict, first_trace_id: str):
    """Store all 7 scores to Langfuse."""
    config_ids = {
        "goal_achievement": "68cfd90c-8c9e-4907-808d-869ccd9a4c07",
        "tool_efficiency": "84965473-0f54-4248-999e-7b8627fc9c29",
        "process_adherence": "651fc213-4750-4d4e-8155-270235c7cad8",
        "context_efficiency": "ae22abed-bd4a-4926-af74-8d71edb1925d",
        "error_handling": "96c290b7-e3a6-4caa-bace-93cf55f70f1c",
        "output_quality": "d33b1fbf-d3c6-458c-90ca-0b515fe09aed",
        "overall_quality": "793f09d9-0053-4310-ad32-00dc06c69a71",
    }

    categorical_dims = ["goal_achievement", "error_handling"]

    for dim, config_id in config_ids.items():
        if dim == "overall_quality":
            continue  # Handle separately

        score_data = scores.get(dim, {})
        value = score_data.get("score", 0)
        rationale = score_data.get("rationale", "")

        # Build CLI command
        cmd = [
            "python", "03-skills/langfuse/langfuse-create-score/scripts/create_score.py",
            "--trace-id", first_trace_id,
            "--name", dim,
            "--value", str(value),
            "--comment", rationale,
        ]

        if dim in categorical_dims:
            label = score_data.get("label", "")
            cmd.extend(["--string-value", label])

        # Execute command
        subprocess.run(cmd, check=True)
```

#### 2.2 SKILL.md
```markdown
# langfuse-score-session

Score a Claude Code session across 6 quality dimensions using the general-purpose subagent.

## Trigger
- "score session"
- "evaluate session"
- "analyze session quality"

## Usage

### Via CLI
```bash
# Score a specific session
python 00-system/skills/meta/langfuse-score-session/scripts/score_session.py --session-id {id}

# Score with dry-run (don't store to Langfuse)
python 00-system/skills/meta/langfuse-score-session/scripts/score_session.py --session-id {id} --dry-run
```

### Via Task Tool (Internal)
The skill spawns a general-purpose subagent with scoring instructions:
```
Task(subagent_type="general-purpose", prompt="FIRST: Read 00-system/skills/meta/langfuse-score-session/prompts/scorer-prompt.md THEN: Score session {id}")
```

## Output
7 scores stored to the session's first trace in Langfuse:
- goal_achievement (CATEGORICAL)
- tool_efficiency (NUMERIC)
- process_adherence (NUMERIC)
- context_efficiency (NUMERIC)
- error_handling (CATEGORICAL)
- output_quality (NUMERIC)
- overall_quality (NUMERIC - weighted aggregate)

## Dependencies
- Langfuse running at localhost:3002
- Score configs from Project 35
- Scoring prompt at `00-system/skills/meta/langfuse-score-session/prompts/scorer-prompt.md`
```

---

## Phase 3: Validation (1 session)

### Goals
- Test on diverse sessions
- Measure performance (time, cost)
- Validate scoring accuracy

### Test Plan

| Test Case | Session Size | Expected |
|-----------|--------------|----------|
| Small session | 5-10 traces | <30 sec, single subagent call |
| Medium session | 20-40 traces | <60 sec, single subagent call |
| Large session | 50+ traces | Sampling, metadata notes |
| Error-heavy | Many failures | Low error_handling score |
| Clean execution | No errors | High process_adherence |

### Sessions to Test
- Pick 5 sessions with varying characteristics
- Document IDs in 04-steps.md
- Compare AI scores with manual review for 2-3 sessions

### Metrics
| Metric | Target |
|--------|--------|
| Time (small) | <30 sec |
| Time (medium) | <60 sec |
| Time (large) | <2 min |
| Cost per session | <$0.15 |

---

## Success Criteria

- [x] Skill created (`00-system/skills/meta/langfuse-score-session/`)
- [ ] Subagent successfully fetches and scores session
- [ ] Orchestrator skill created
- [ ] Overall quality calculation works
- [ ] Scores stored correctly to Langfuse (including CATEGORICAL with string_value)
- [ ] Tested on 5+ diverse sessions
- [ ] Performance documented

---

## Dependencies (SATISFIED)

| Dependency | Status |
|------------|--------|
| Project 35 - Score Configs | COMPLETE |
| Langfuse running | Available |
| Scoring skill + prompt | CREATED |
| Langfuse skills (get-session, etc.) | Available |

---

## Output Artifacts

After completion:
- `03-skills/langfuse/langfuse-score-session/` - Complete skill
- `03-working/subagent-testing.md` - Testing notes
- `04-outputs/validation-results.md` - Test results
- `04-outputs/performance-metrics.md` - Time/cost analysis

---

## Reference Materials

- `00-system/skills/meta/langfuse-score-session/prompts/scorer-prompt.md` - Scoring instructions
- `02-resources/reference/config-ids.md` - Langfuse config IDs
- `02-resources/reference/enhanced-scoring-design.md` - Full dimension specs
- `02-resources/reference/p35-setup-complete.md` - P35 learnings

---

*Ready for execution. See 04-steps.md for granular task tracking.*
