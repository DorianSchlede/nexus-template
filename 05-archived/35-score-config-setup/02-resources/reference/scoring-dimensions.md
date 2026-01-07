# Scoring Dimensions (Enhanced)

**Version**: 2.0
**Date**: 2026-01-07
**Supersedes**: Original 7-dimension design from Project 27

---

## Summary

This document defines **6 enhanced scoring dimensions** designed for:
- **Measurability**: Partial auto-signals from trace data
- **Actionability**: Low scores point to specific improvements
- **Nexus-awareness**: Dimensions reflect Nexus system patterns
- **Non-overlap**: Each dimension measures something distinct

**Architecture**: Multi-critic subagent scoring (see Project 36)

---

## Dimension 1: Goal Achievement

**Name**: `goal_achievement`
**Type**: CATEGORICAL
**Categories**: `failed` (0), `partial` (1), `complete` (2), `exceeded` (3)
**Weight**: 0.30 (highest - outcomes matter most)
**Critic**: Goal Critic (sonnet)

### What It Measures
Did the session accomplish what the user asked for?

### Scoring Criteria

| Score | Criteria |
|-------|----------|
| failed (0) | Goal not achieved, session abandoned or blocked |
| partial (1) | Some progress but incomplete delivery |
| complete (2) | Goal achieved as requested |
| exceeded (3) | Goal achieved + proactive improvements |

### Evidence to Look For

**Good patterns (+)**:
- Clear task completion signal in final traces
- Explicit completion signals ("done", "thanks", commit created)
- Deliverables created (files written, tests passing)
- User confirmation received

**Bad patterns (-)**:
- Session ended mid-task
- Missing deliverables
- Unresolved blockers
- Abandoned without explanation

### Measurement Approach
- Extract task context from first user message
- Check for completion markers in final traces
- Verify deliverables created/modified
- Look for user satisfaction signals

---

## Dimension 2: Tool Efficiency

**Name**: `tool_efficiency`
**Type**: NUMERIC (0.0 - 1.0)
**Weight**: 0.20
**Critic**: Tool Critic (haiku)

### What It Measures
Did the session use the right tools effectively?

### Scoring Criteria

| Score | Criteria |
|-------|----------|
| 0.0-0.3 | Wrong tools, many retries, Bash for file ops |
| 0.4-0.6 | Some misuse, moderate retries |
| 0.7-0.8 | Generally correct, few retries |
| 0.9-1.0 | Optimal tool selection, parallel where possible |

### Evidence to Look For

**Good patterns (+)**:
- Used Read for file reading (not cat via Bash)
- Used Edit for modifications (not sed/awk)
- Used Grep for search (not grep via Bash)
- Used Task tool for exploration
- Parallel tool calls when independent
- Quick pivot on errors

**Bad patterns (-)**:
- Used Bash for file operations
- Excessive tool retries
- Wrong tool for job (e.g., Write when Edit needed)
- Repeated same failing command
- Sequential calls when parallel possible

### Auto-Measurable Signals
```python
tool_efficiency = 1 - (retry_count / total_tool_calls)
bash_penalty = bash_file_ops / total_file_ops * 0.2
parallel_bonus = parallel_calls / total_independent_calls * 0.1
```

---

## Dimension 3: Process Adherence

**Name**: `process_adherence`
**Type**: NUMERIC (0.0 - 1.0)
**Weight**: 0.20
**Critic**: Process Critic (haiku)

### What It Measures
Did the session follow proper Nexus workflows?

### Scoring Criteria

| Score | Criteria |
|-------|----------|
| 0.0-0.3 | Ignored workflows, no planning, chaotic execution |
| 0.4-0.6 | Some process followed, gaps in discipline |
| 0.7-0.8 | Good process adherence, minor deviations |
| 0.9-1.0 | Exemplary workflow execution, proper patterns |

### Evidence to Look For

**Good patterns (+)**:
- TodoWrite used for multi-step tasks
- Read before Edit pattern followed
- Skill loaded via proper patterns (Skill tool, not Bash)
- Project workflow followed (execute-project steps)
- Proper routing via orchestrator rules

**Bad patterns (-)**:
- Skipped TodoWrite for complex tasks
- Edit without prior Read
- Manual skill loading via Bash
- Ignored project steps.md
- Bypassed Nexus routing

### Auto-Measurable Signals
```python
has_todo = "TodoWrite" in trace_tools
read_before_edit = check_read_edit_pattern(traces)
proper_skill_load = not uses_bash_for_skill_load(traces)
```

---

## Dimension 4: Context Efficiency

**Name**: `context_efficiency`
**Type**: NUMERIC (0.0 - 1.0)
**Weight**: 0.15
**Critic**: Tool Critic (haiku)

### What It Measures
How efficiently was context/tokens used?

### Scoring Criteria

| Score | Criteria |
|-------|----------|
| 0.0-0.3 | Excessive file loading, many re-reads, bloated context |
| 0.4-0.6 | Some redundancy, moderate inefficiency |
| 0.7-0.8 | Reasonable context usage, minor waste |
| 0.9-1.0 | Minimal context, targeted reads, good delegation |

### Evidence to Look For

**Good patterns (+)**:
- Loaded only needed files
- Used targeted Glob/Grep before reading
- Avoided re-reading same files
- Used file offsets for large files
- Used Task tool for exploration (not bloating main context)
- Direct path to solution

**Bad patterns (-)**:
- Read same file multiple times
- Full file reads when partial would suffice
- Excessive startup context bloat
- Loaded entire skill when only needed one section
- Unnecessary exploration in main context

### Auto-Measurable Signals
```python
unique_files_read = len(set(files_read))
total_reads = len(files_read)
read_efficiency = unique_files_read / total_reads
task_delegation = "Task" in tools and "explore" in prompts
```

---

## Dimension 5: Error Handling

**Name**: `error_handling`
**Type**: CATEGORICAL
**Categories**: `poor` (0), `struggled` (1), `recovered` (2), `prevented` (3)
**Weight**: 0.10
**Critic**: Goal Critic (sonnet)

### What It Measures
How were errors and blockers handled?

### Scoring Criteria

| Score | Criteria |
|-------|----------|
| poor (0) | Repeated same failing command, ignored errors |
| struggled (1) | Eventually recovered but took many attempts |
| recovered (2) | Quick pivot on errors, good debugging |
| prevented (3) | Proactive checks prevented errors, clean execution |

### Evidence to Look For

**Good patterns (+)**:
- Quick pivot strategies after failures
- Proactive error prevention (checks before actions)
- Escalation to user when appropriate
- Smart debugging (read error messages, adjust approach)

**Bad patterns (-)**:
- Repeated same failing command multiple times
- Ignored error messages
- Cascading failures
- No adaptation after errors

---

## Dimension 6: Output Quality

**Name**: `output_quality`
**Type**: NUMERIC (0.0 - 1.0)
**Weight**: 0.05
**Critic**: Quality Critic (haiku)

### What It Measures
Quality of the actual deliverables produced.

### Scoring Criteria

| Score | Criteria |
|-------|----------|
| 0.0-0.3 | Broken output, syntax errors, poor formatting |
| 0.4-0.6 | Functional but rough, minor issues |
| 0.7-0.8 | Good quality, clean output |
| 0.9-1.0 | Excellent quality, polished deliverables |

### Evidence to Look For

**Good patterns (+)**:
- Code compiles/runs (if applicable)
- Tests pass (if modified)
- Markdown formatting correct
- File references use proper links (VSCode `[file](path)`)
- No unnecessary emojis (unless requested)
- Concise, focused responses

**Bad patterns (-)**:
- Syntax errors in code
- Tests fail after changes
- Broken markdown/formatting
- Debug artifacts left in code
- Verbose, unfocused responses

---

## Aggregate: Overall Quality

**Name**: `overall_quality`
**Type**: NUMERIC (0.0 - 1.0)

### Formula

```python
def calculate_overall_quality(scores: Dict) -> float:
    """Weighted aggregate with categorical normalization."""

    # Normalize categorical to 0-1 (0→0.0, 1→0.33, 2→0.67, 3→1.0)
    def normalize_categorical(value: int) -> float:
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
        value = scores[dim]["score"]
        if dim in ["goal_achievement", "error_handling"]:
            value = normalize_categorical(value)
        total += value * weight

    return round(total, 3)
```

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
    # CATEGORICAL configs
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

    # NUMERIC configs
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

## Multi-Critic Assignment

| Critic | Model | Dimensions |
|--------|-------|------------|
| Goal Critic | sonnet | goal_achievement, error_handling |
| Tool Critic | haiku | tool_efficiency, context_efficiency |
| Process Critic | haiku | process_adherence |
| Quality Critic | haiku | output_quality |

**Rationale**:
- Goal + Error need nuanced judgment → sonnet
- Tool + Context are pattern matching → haiku
- Process is checklist-based → haiku
- Quality is output review → haiku

---

## Comparison: Old vs New Dimensions

| Old (v1) | New (v2) | Change |
|----------|----------|--------|
| task_completion | goal_achievement | Renamed for clarity |
| execution_quality | process_adherence | More specific (workflow focus) |
| tool_mastery | tool_efficiency | More measurable |
| resource_efficiency | context_efficiency | More specific (context focus) |
| security_compliance | *(removed)* | Rare signal, low value |
| user_satisfaction | *(removed)* | Proxy for goal_achievement |
| *(new)* | error_handling | Critical gap filled |
| *(new)* | output_quality | Deliverable focus |
| overall_quality | overall_quality | Same (formula updated) |

---

*Ready for implementation in Project 35 (configs) and Project 36 (scorer)*
