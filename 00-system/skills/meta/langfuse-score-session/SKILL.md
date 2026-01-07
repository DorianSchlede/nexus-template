# langfuse-score-session

Score a Claude Code session across 6 quality dimensions using a subagent.

## Trigger

- "score session"
- "evaluate session quality"
- "analyze session"

## Usage

### Step 1: Invoke Subagent

Use the Task tool with `general-purpose` and instruct it to read the scoring prompt:

```
Task(
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

### Step 2: Parse JSON Output

The subagent returns JSON with:
- 6 dimension scores
- root_cause analysis
- improvement suggestions
- session_notes
- metadata

### Step 3: Calculate Overall Quality

```python
def calculate_overall_quality(scores):
    def normalize_cat(v): return v / 3.0

    return (
        normalize_cat(scores["goal_achievement"]["score"]) * 0.30 +
        scores["tool_efficiency"]["score"] * 0.20 +
        scores["process_adherence"]["score"] * 0.20 +
        scores["context_efficiency"]["score"] * 0.15 +
        normalize_cat(scores["error_handling"]["score"]) * 0.10 +
        scores["output_quality"]["score"] * 0.05
    )
```

### Step 4: Store Scores to Langfuse

Get the first trace ID from the session, then store all scores:

```bash
# Get first trace
python 03-skills/langfuse/langfuse-list-traces/scripts/list_traces.py --session-id {session_id} --limit 1

# Store each score (example for tool_efficiency)
python 03-skills/langfuse/langfuse-create-score/scripts/create_score.py \
    --trace-id {first_trace_id} \
    --name "tool_efficiency" \
    --value 0.85 \
    --comment "Good tool selection..."

# For CATEGORICAL scores, add --string-value
python 03-skills/langfuse/langfuse-create-score/scripts/create_score.py \
    --trace-id {first_trace_id} \
    --name "goal_achievement" \
    --value 2 \
    --string-value "complete" \
    --comment "Goal achieved as requested"
```

## Dependencies

### Langfuse Skills
- `langfuse-list-traces` - Get traces in session
- `langfuse-get-trace` - Get trace details
- `langfuse-create-score` - Store scores

### Files
- `prompts/scorer-prompt.md` - Scoring instructions for subagent

### Score Config IDs

```python
CONFIG_IDS = {
    "goal_achievement": "68cfd90c-8c9e-4907-808d-869ccd9a4c07",
    "tool_efficiency": "84965473-0f54-4248-999e-7b8627fc9c29",
    "process_adherence": "651fc213-4750-4d4e-8155-270235c7cad8",
    "context_efficiency": "ae22abed-bd4a-4926-af74-8d71edb1925d",
    "error_handling": "96c290b7-e3a6-4caa-bace-93cf55f70f1c",
    "output_quality": "d33b1fbf-d3c6-458c-90ca-0b515fe09aed",
    "overall_quality": "793f09d9-0053-4310-ad32-00dc06c69a71",
    "root_cause_issues": "669bead7-1936-4fc4-bae8-e7814c9eab04",
    "session_improvements": "2e87193b-c853-4955-b2f0-9fa572531681",
    "session_notes": "67640329-0c03-4be6-bc9f-49765a0462b5",
}
```

## Output

10 scores stored to the session's first trace:
- 6 quality dimensions
- 1 overall_quality (weighted aggregate)
- 1 root_cause_issues
- 1 session_improvements
- 1 session_notes
