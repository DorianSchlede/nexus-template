# Project 36: Execution Steps

**Last Updated**: 2026-01-07
**Status**: IN_PROGRESS (Phase 1 ready to start)

**IMPORTANT**: Mark tasks complete with [x] as you finish them.

---

## Phase 0: Project Setup (COMPLETE)

- [x] Create project folder structure
- [x] Copy reference files from Project 27
- [x] Write 01-overview.md with system context
- [x] Write 02-discovery.md with initial findings
- [x] Write 03-plan.md with execution strategy
- [x] Write 04-steps.md (this file)
- [x] Create scorer prompt (`00-system/skills/meta/langfuse-score-session/prompts/scorer-prompt.md`)
- [x] Copy P35 outputs to resources (enhanced-scoring-design.md, config-ids.md, p35-setup-complete.md)
- [x] Align all plan files with P35 dimensions

---

## Phase 1: Subagent Testing (CURRENT)

### 1.1 Find Test Session
- [x] List recent sessions from Langfuse
- [x] Pick a small session (5-10 traces) for testing
- [x] Document session_id: `282286a0f66de884760184bc6aab291e` (10 traces, subagent research session)

### 1.2 Test Subagent Invocation
- [x] Spawn scorer via general-purpose subagent with prompt file read
- [x] Verify subagent reads scoring instructions
- [x] Verify subagent fetches from Langfuse
- [x] Check for any errors in invocation

### 1.3 Validate Output
- [x] Verify JSON output matches schema
- [x] Check all 6 dimensions are scored
- [x] Verify evidence is cited from traces
- [x] Verify rationales are present
- [x] Check metadata (confidence, notes)

### 1.4 Document Findings
- [x] Create `03-working/subagent-testing.md`
- [x] Note any issues or adjustments needed
- [x] Create `03-working/key-learnings.md` with architecture decisions

---

## Phase 2: Orchestrator Implementation

### 2.1 Score Session CLI
- [x] Create `00-system/skills/meta/langfuse-score-session/` folder structure
- [ ] Create `scripts/score_session.py` CLI
- [ ] Implement `calculate_overall_quality()` function
- [ ] Test calculation with mock data

### 2.2 Score Storage
- [ ] Implement NUMERIC score storage
- [ ] Implement CATEGORICAL score storage (with string_value)
- [ ] Test storing single score to Langfuse
- [ ] Test storing all 7 scores

### 2.3 Skill Definition
- [x] Create `SKILL.md` with usage examples
- [ ] Document CLI options (--session-id, --dry-run)
- [ ] Add troubleshooting section

### 2.4 End-to-End Test
- [ ] Run full pipeline on test session
- [ ] Verify scores appear in Langfuse UI
- [ ] Check score values are correct
- [ ] Verify overall_quality calculation

---

## Phase 3: Validation

### 3.1 Test Diverse Sessions
- [ ] Score Session 1 (small, 5-10 traces): ________________
- [ ] Score Session 2 (medium, 20-40 traces): ________________
- [ ] Score Session 3 (error-heavy): ________________
- [ ] Score Session 4 (clean execution): ________________
- [ ] Score Session 5 (large, 50+ traces): ________________

### 3.2 Measure Performance
- [ ] Record time for each session
- [ ] Record cost for each session
- [ ] Compare against targets

### 3.3 Human Calibration
- [ ] Manually score 2-3 sessions
- [ ] Compare AI vs human scores
- [ ] Document disagreements

### 3.4 Documentation
- [ ] Create `04-outputs/validation-results.md`
- [ ] Create `04-outputs/performance-metrics.md`
- [ ] Update resume-context.md

---

## Notes

### Score Config IDs (from Project 35 + Project 36)

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
    # Root Cause & Improvements (NEW - Project 36)
    "root_cause_issues": "669bead7-1936-4fc4-bae8-e7814c9eab04",
    "session_improvements": "2e87193b-c853-4955-b2f0-9fa572531681",
}

DATASET_ID = "cmk4aug97000eqg070ila53nw"
```

### Scoring Dimensions

| Dimension | Type | Weight | Categories (if CATEGORICAL) |
|-----------|------|--------|----------------------------|
| goal_achievement | CATEGORICAL | 0.30 | failed(0), partial(1), complete(2), exceeded(3) |
| tool_efficiency | NUMERIC | 0.20 | 0.0-1.0 |
| process_adherence | NUMERIC | 0.20 | 0.0-1.0 |
| context_efficiency | NUMERIC | 0.15 | 0.0-1.0 |
| error_handling | CATEGORICAL | 0.10 | poor(0), struggled(1), recovered(2), prevented(3) |
| output_quality | NUMERIC | 0.05 | 0.0-1.0 |
| overall_quality | NUMERIC | - | 0.0-1.0 (weighted aggregate) |

### Root Cause & Improvements (NEW)

| Score | Type | Categories |
|-------|------|------------|
| root_cause_issues | CATEGORICAL | none(0), tool_misuse(1), process_violation(2), context_waste(3), error_cascade(4), output_quality(5), multiple(6) |
| session_improvements | CATEGORICAL | none(0), minor(1), moderate(2), significant(3), critical(4) |

**Note**: `session_improvements` comment field contains JSON array: `[{dimension, issue, fix}, ...]`

### Overall Quality Formula

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

### Test Session IDs (fill during validation)
- Test Session (Phase 1): `282286a0f66de884760184bc6aab291e`
- Small Session: ________________
- Medium Session: ________________
- Error-heavy Session: ________________
- Clean Session: ________________
- Large Session: ________________

---

*Mark tasks complete with [x] as you finish them*
