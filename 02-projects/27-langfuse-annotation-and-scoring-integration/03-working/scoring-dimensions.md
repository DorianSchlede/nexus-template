# Scoring Dimensions

**Phase**: 5 (Pattern Identification)
**Date**: 2026-01-05
**Updated**: 2026-01-05 (Post-Validation Revision)

---

## Summary

Based on manual review of 3 sessions and **post-validation analysis**, these scoring dimensions represent the refined framework. Key changes from original:
- Merged `context_efficiency` + `cost_efficiency` → `resource_efficiency` (85% correlation)
- Merged `tool_appropriateness` + `error_recovery` → `tool_mastery`
- Added `security_compliance` (critical gap identified)
- Added `user_satisfaction` (available from trace data)

---

## Dimension 1: Task Completion

**Name**: `task_completion`
**Type**: CATEGORICAL
**Categories**: failed (0), partial (1), complete (2), exceeded (3)
**Weight**: 0.30 (highest - outcomes matter most)
**Description**: Did the session achieve its objective?

### Scoring Criteria

| Score | Criteria |
|-------|----------|
| failed | Task not completed, major blockers |
| partial | Some progress, task incomplete |
| complete | Task finished as requested |
| exceeded | Completed task + proactive improvements |

### Indicators

**Good patterns** (+):
- Clear task completion signal
- All requested items delivered
- User confirmation received
- Proper close-session triggered

**Bad patterns** (-):
- Session ended mid-task
- Missing deliverables
- Unresolved blockers
- Abandoned without explanation

### Measurement Approach
- Check for completion markers in final traces
- Verify deliverables created/modified
- Look for user satisfaction signals
- **Requires task context extraction** from first user message

---

## Dimension 2: Execution Quality

**Name**: `execution_quality`
**Type**: NUMERIC (0.0 - 1.0)
**Weight**: 0.25
**Description**: How well were instructions followed and work executed? (Replaces `instruction_following`)

### Scoring Criteria

| Score | Criteria |
|-------|----------|
| 0.0-0.3 | Ignored instructions, deviated significantly, poor work quality |
| 0.4-0.6 | Followed some instructions, missed others, uneven quality |
| 0.7-0.8 | Followed most instructions with minor deviations |
| 0.9-1.0 | Precisely followed all instructions, high quality output |

### Indicators

**Good patterns** (+):
- Followed SKILL.md workflow steps in order
- Executed project tasks as defined in steps.md
- Respected user constraints and preferences
- Used TodoWrite to track progress
- Clean, well-structured outputs

**Bad patterns** (-):
- Skipped skill workflow steps
- Ignored user corrections
- Proceeded without required context
- Deviated from defined plan
- Sloppy or incomplete outputs

### Measurement Approach
- Compare actions taken vs instructions loaded
- Check if TodoWrite reflects actual work done
- Verify skill steps were executed in order
- Assess output quality

---

## Dimension 3: Tool Mastery

**Name**: `tool_mastery`
**Type**: NUMERIC (0.0 - 1.0)
**Weight**: 0.20
**Description**: Were the right tools used effectively, and were errors handled well? (Merges `tool_appropriateness` + `error_recovery`)

### Scoring Criteria

| Score | Criteria |
|-------|----------|
| 0.0-0.3 | Wrong tools, many failures, poor error handling |
| 0.4-0.6 | Some tool misuse, slow error recovery |
| 0.7-0.8 | Generally correct tools, adequate error handling |
| 0.9-1.0 | Optimal tool selection, excellent error recovery |

### Indicators

**Good patterns** (+):
- Used Read for file reading (not cat via Bash)
- Used Edit for modifications (not sed/awk)
- Used Grep for search (not grep via Bash)
- Used Task tool for complex exploration
- Quick pivot on errors, smart debugging
- Didn't repeat failed attempts

**Bad patterns** (-):
- Used Bash for file operations
- Excessive tool retries
- Wrong tool for job (e.g., Write when Edit needed)
- Repeated same failing command
- Ignored error messages
- Cascading failures

### Measurement Approach
- Analyze tool call sequences
- Check for tool failures and retries
- Count error occurrences and recovery time
- Compare tool choices to best practices

---

## Dimension 4: Resource Efficiency

**Name**: `resource_efficiency`
**Type**: NUMERIC (0.0 - 1.0)
**Weight**: 0.15
**Description**: How efficiently were context and tokens used? (Merges `context_efficiency` + `cost_efficiency`)

### Scoring Criteria

| Score | Criteria |
|-------|----------|
| 0.0-0.3 | Excessive context loading, wasteful token usage |
| 0.4-0.6 | Some redundancy, moderately expensive |
| 0.7-0.8 | Reasonable resource usage, minor inefficiencies |
| 0.9-1.0 | Optimal context loading, efficient execution |

### Indicators

**Good patterns** (+):
- Loaded only needed files
- Used targeted Glob/Grep before reading
- Avoided re-reading same files
- Used file offsets for large files
- Direct path to solution
- Minimal context switching

**Bad patterns** (-):
- Read same file multiple times
- Loaded entire skill when only needed one section
- Full file reads when partial would suffice
- Excessive startup context bloat
- Unnecessary exploration
- High token count for simple task

### Measurement Approach
- Count unique files read vs total file read operations
- Estimate tokens loaded vs tokens actually used
- Calculate cost/trace ratio
- **Note**: Input tokens currently not tracked (OTEL fix required)

---

## Dimension 5: Security Compliance

**Name**: `security_compliance`
**Type**: CATEGORICAL
**Categories**: violation (0), risk (1), compliant (2), exemplary (3)
**Weight**: 0.05
**Description**: Did the session avoid security risks? (NEW - critical gap identified in validation)

### Scoring Criteria

| Score | Criteria |
|-------|----------|
| violation | Exposed secrets, credentials, or PII in outputs |
| risk | Handled sensitive data but with some exposure risk |
| compliant | No security issues, followed safe practices |
| exemplary | Proactively identified and mitigated security risks |

### Indicators

**Good patterns** (+):
- Did not echo/log credentials
- Used environment variables for secrets
- Warned about .env files in commits
- Avoided hardcoding API keys
- Sanitized user inputs

**Bad patterns** (-):
- Printed API keys or tokens
- Committed credentials to git
- Exposed PII in logs or outputs
- Used insecure patterns (SQL injection risk, etc.)
- Ignored security warnings

### Measurement Approach
- Pattern match for API key formats in outputs
- Check for .env, credentials.json in git operations
- Scan for common secret patterns
- Verify secure coding practices

---

## Dimension 6: User Satisfaction

**Name**: `user_satisfaction`
**Type**: CATEGORICAL
**Categories**: frustrated (0), neutral (1), satisfied (2), delighted (3)
**Weight**: 0.05
**Description**: How did the user respond to the session? (NEW - available from trace data)

### Scoring Criteria

| Score | Criteria |
|-------|----------|
| frustrated | User expressed frustration, corrections ignored |
| neutral | No clear satisfaction signals |
| satisfied | User confirmed completion, said thanks |
| delighted | User expressed enthusiasm, praised work |

### Indicators

**Good patterns** (+):
- User says "thanks", "great", "perfect"
- User confirms task completion
- No corrections or complaints
- User continues with follow-up work

**Bad patterns** (-):
- User says "no", "wrong", "not what I asked"
- Multiple corrections in session
- User abandons session
- User re-explains same thing

### Measurement Approach
- Sentiment analysis on user messages
- Count correction/rejection patterns
- Check for explicit satisfaction signals
- Analyze session ending pattern

---

## Session-Level Aggregate Scores

### Overall Quality Score

**Formula**: Weighted average of dimensions

```
overall = (
    task_completion * 0.30 +
    execution_quality * 0.25 +
    tool_mastery * 0.20 +
    resource_efficiency * 0.15 +
    security_compliance * 0.05 +
    user_satisfaction * 0.05
)
```

**Normalization**: Categorical scores mapped to 0-1:
- 0 → 0.0
- 1 → 0.33
- 2 → 0.67
- 3 → 1.0

### Quality Tiers

| Tier | Score Range | Interpretation |
|------|-------------|----------------|
| Excellent | 0.85-1.0 | Model session, use as example |
| Good | 0.70-0.84 | Solid performance, minor issues |
| Acceptable | 0.50-0.69 | Completed but inefficient |
| Poor | 0.30-0.49 | Significant issues, needs review |
| Failed | 0.0-0.29 | Major problems, investigate |

---

## Score Configs for Langfuse

```python
SCORE_CONFIGS = [
    {
        "name": "task_completion",
        "dataType": "CATEGORICAL",
        "categories": [
            {"label": "failed", "value": 0},
            {"label": "partial", "value": 1},
            {"label": "complete", "value": 2},
            {"label": "exceeded", "value": 3}
        ],
        "description": "Whether the task was completed"
    },
    {
        "name": "execution_quality",
        "dataType": "NUMERIC",
        "minValue": 0,
        "maxValue": 1,
        "description": "How well instructions were followed and work executed"
    },
    {
        "name": "tool_mastery",
        "dataType": "NUMERIC",
        "minValue": 0,
        "maxValue": 1,
        "description": "Tool selection and error recovery quality"
    },
    {
        "name": "resource_efficiency",
        "dataType": "NUMERIC",
        "minValue": 0,
        "maxValue": 1,
        "description": "Context and token efficiency"
    },
    {
        "name": "security_compliance",
        "dataType": "CATEGORICAL",
        "categories": [
            {"label": "violation", "value": 0},
            {"label": "risk", "value": 1},
            {"label": "compliant", "value": 2},
            {"label": "exemplary", "value": 3}
        ],
        "description": "Security and credential handling"
    },
    {
        "name": "user_satisfaction",
        "dataType": "CATEGORICAL",
        "categories": [
            {"label": "frustrated", "value": 0},
            {"label": "neutral", "value": 1},
            {"label": "satisfied", "value": 2},
            {"label": "delighted", "value": 3}
        ],
        "description": "User response and satisfaction signals"
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

## Session Completeness Criteria

A session is "complete" (vs "abandoned") if:

1. **Has clear ending**:
   - close-session triggered
   - User says "done", "thanks", etc.
   - Task explicitly completed

2. **Deliverables present**:
   - Files created/modified as expected
   - Output artifacts generated

3. **No hanging state**:
   - No unresolved errors
   - No pending questions

### Filtering Incomplete Sessions

For batch scoring, exclude sessions that:
- Have < 3 traces (likely false starts)
- End mid-sentence (context cutoff)
- Have no user messages after startup

---

## Validation Notes

**Post-validation changes made**:

1. **Merged dimensions**: Reduced from 6 to 6 (but 2 new, 2 merged)
   - `context_efficiency` + `cost_efficiency` → `resource_efficiency` (0.85 correlation)
   - `tool_appropriateness` + `error_recovery` → `tool_mastery`

2. **Added critical dimensions**:
   - `security_compliance` - prevents credential leaks
   - `user_satisfaction` - captures user feedback signals

3. **Reweighted**:
   - `task_completion` increased to 0.30 (outcomes matter most)
   - New dimensions at 0.05 each (important but secondary)

4. **Type changes**:
   - `instruction_following` → `execution_quality` (NUMERIC for finer granularity)

---

*Updated after ULTRAVALIDATION - ready for implementation*
