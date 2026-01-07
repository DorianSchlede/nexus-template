# Score Config IDs

**Created**: 2026-01-07
**Updated**: 2026-01-07 (Added root_cause_issues, session_improvements)
**Project**: cmk05cowc0006nt0752qjtfj2

---

## Production Score Configs

### Quality Dimensions (from Project 35)

| Dimension | Type | ID |
|-----------|------|-----|
| goal_achievement | CATEGORICAL | `68cfd90c-8c9e-4907-808d-869ccd9a4c07` |
| tool_efficiency | NUMERIC | `84965473-0f54-4248-999e-7b8627fc9c29` |
| process_adherence | NUMERIC | `651fc213-4750-4d4e-8155-270235c7cad8` |
| context_efficiency | NUMERIC | `ae22abed-bd4a-4926-af74-8d71edb1925d` |
| error_handling | CATEGORICAL | `96c290b7-e3a6-4caa-bace-93cf55f70f1c` |
| output_quality | NUMERIC | `d33b1fbf-d3c6-458c-90ca-0b515fe09aed` |
| overall_quality | NUMERIC | `793f09d9-0053-4310-ad32-00dc06c69a71` |

### Root Cause & Improvements (from Project 36)

| Dimension | Type | ID | Categories |
|-----------|------|-----|------------|
| root_cause_issues | CATEGORICAL | `669bead7-1936-4fc4-bae8-e7814c9eab04` | none, tool_misuse, process_violation, context_waste, error_cascade, output_quality, multiple |
| session_improvements | CATEGORICAL | `2e87193b-c853-4955-b2f0-9fa572531681` | none, minor, moderate, significant, critical |

---

## Dataset

| Name | ID |
|------|-----|
| quality-monitoring-ground-truth | `cmk4aug97000eqg070ila53nw` |

---

## Test Configs (from Project 27)

| Name | Type | ID |
|------|------|-----|
| test-efficiency | NUMERIC | `44cb8474-9898-4b35-a825-70d1a4ea2c52` |
| test-quality | CATEGORICAL | `ba02dae1-7b6c-4401-b13a-afb6df23c35d` |

---

## Usage in Code

```python
CONFIG_IDS = {
    # 6 Quality Dimensions
    "goal_achievement": "68cfd90c-8c9e-4907-808d-869ccd9a4c07",
    "tool_efficiency": "84965473-0f54-4248-999e-7b8627fc9c29",
    "process_adherence": "651fc213-4750-4d4e-8155-270235c7cad8",
    "context_efficiency": "ae22abed-bd4a-4926-af74-8d71edb1925d",
    "error_handling": "96c290b7-e3a6-4caa-bace-93cf55f70f1c",
    "output_quality": "d33b1fbf-d3c6-458c-90ca-0b515fe09aed",
    # Aggregate
    "overall_quality": "793f09d9-0053-4310-ad32-00dc06c69a71",
    # Root Cause & Improvements
    "root_cause_issues": "669bead7-1936-4fc4-bae8-e7814c9eab04",
    "session_improvements": "2e87193b-c853-4955-b2f0-9fa572531681",
}

DATASET_ID = "cmk4aug97000eqg070ila53nw"
```

---

## Score Storage Pattern

```python
# Quality dimension scores (6 + 1 aggregate)
for dim in ["goal_achievement", "tool_efficiency", ...]:
    langfuse.create_score(trace_id, dim, value, comment=rationale)

# Root cause (CATEGORICAL - needs string_value)
langfuse.create_score(
    trace_id=trace_id,
    name="root_cause_issues",
    value=1,  # numeric value
    string_value="tool_misuse",  # REQUIRED for CATEGORICAL
    comment="Primary issue: Used Bash for file reading instead of Read tool"
)

# Session improvements (CATEGORICAL - comment contains JSON suggestions)
langfuse.create_score(
    trace_id=trace_id,
    name="session_improvements",
    value=2,  # moderate
    string_value="moderate",
    comment='[{"dimension": "tool_efficiency", "issue": "Bash for file ops", "fix": "Use Read tool"}]'
)
```
