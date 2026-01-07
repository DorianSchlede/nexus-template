# Selected Traces for Calibration

**Date**: 2026-01-07
**Purpose**: Identify traces for test-case-analyzer calibration dataset

---

## Selection Criteria

Per discovery requirements:
1. Mix of PASS/FAIL expected outcomes
2. At least 5 traces minimum
3. Traces with observations (tool calls) for evaluation
4. Prefer traces with existing scores for comparison

---

## Selected Sessions

### Session 1: agent-a000241 (SCORED)
- **Session ID**: `358deea93f6499d3936ed925e1e2f588`
- **Trace Count**: 19
- **Observations**: 1
- **Has Scores**: YES (7 scores from session-scorer)
- **Date**: 2026-01-07
- **Expected Outcome**: PASS (completed skill validation)
- **Selection Rationale**: Only session with existing scores, represents successful validation run

### Session 2: agent-a9cda74 (Research)
- **Session ID**: `282286a0f66de884760184bc6aab291e`
- **Trace Count**: 17
- **Observations**: 2
- **Has Scores**: NO
- **Date**: 2026-01-07
- **Expected Outcome**: PASS (information retrieval task)
- **Selection Rationale**: Longest conversation, diverse tool usage

### Session 3: agent-aa40d86
- **Session ID**: `7df40ccd016c8533d360207ce87af833`
- **Trace Count**: 7
- **Observations**: 2
- **Has Scores**: NO
- **Date**: 2026-01-07
- **Expected Outcome**: TBD (needs review)
- **Selection Rationale**: Medium-length session with observations

### Session 4: agent-aae376a
- **Session ID**: `d0b569745839a0406b62b42e36e8ee79`
- **Trace Count**: 5
- **Observations**: 2
- **Has Scores**: NO
- **Date**: 2026-01-07
- **Expected Outcome**: TBD (needs review)
- **Selection Rationale**: Shorter session, good for edge case testing

### Session 5: agent-a2251e1 (Long session)
- **Session ID**: `f78d6d837c31773e600931679e007e8a`
- **Trace Count**: 33
- **Observations**: 1
- **Has Scores**: NO
- **Date**: 2026-01-07
- **Expected Outcome**: TBD (needs review)
- **Selection Rationale**: Longest session by trace count, complex workflow

### Session 6: agent-ac130b0 (Project 34 reference)
- **Session ID**: `2ea194d945a98cfca34d1125de5ea9f8`
- **Trace Count**: 9
- **Observations**: 1
- **Has Scores**: NO
- **Date**: 2026-01-07
- **Expected Outcome**: PASS (from discovery doc: skill_structure_check)
- **Selection Rationale**: Referenced in 02-discovery.md as known PASS case

---

## Next Steps

1. **Human Review Required**: Fetch full trace data for each session
2. **Determine Ground Truth**: Review observations to establish PASS/FAIL for each
3. **Identify Edge Cases**: Find or create FAIL/PARTIAL scenarios
4. **Create Dataset Items**: Use langfuse-create-dataset skill

---

## Gaps Identified

Per mental model analysis from planning:

| Gap | Status | Mitigation |
|-----|--------|------------|
| Need FAIL traces | OPEN | May need to create synthetic fail cases |
| Need edge cases | OPEN | Session 4 (short) may serve as edge |
| Criterion assertability | PENDING | Will verify during ground truth creation |

---

## Raw Data Reference

Candidate sessions JSON saved to: `03-working/candidate-sessions.json`

---

*This document will be updated after human review of trace data*
