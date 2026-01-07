# Spawned Project: Ground Truth Bootstrap

**Parent Research**: Project 27 - Langfuse Annotation and Scoring Integration
**Estimated Effort**: Medium (human time - 3-5 sessions spread across 2 weeks)
**Priority**: Medium (needed for calibration, can run in parallel with Project 30)

---

## Purpose

Manually label 50 sessions to create ground truth data for calibrating the AI scorer. This enables measuring and improving AI-human agreement.

---

## Scope

### Must Do
1. Select 50 diverse sessions for labeling
2. Create labeling guidelines document
3. Manually score all 50 sessions across 6 dimensions
4. Store labels in Langfuse ground truth dataset
5. Calculate baseline AI-human agreement metrics
6. Document calibration findings

### Out of Scope
- Adjusting scorer prompts (future iteration)
- Building calibration UI (manual via Langfuse)
- Ongoing human labeling (establish process, not ongoing)

---

## Dependencies

**Requires**:
- Score configs in Langfuse (Project 28)
- Ground truth dataset created (Project 28)
- SessionScorer working (Project 29) - for comparison

**Enables**:
- Scorer calibration and improvement
- Confidence in automated scores
- Bias detection

---

## Session Selection Strategy

### Diversity Requirements

Select 50 sessions with distribution:

**By size**:
- 15 small (<10 traces)
- 20 medium (10-50 traces)
- 15 large (50+ traces)

**By type** (based on project/skill):
- 15 project execution sessions
- 15 skill execution sessions
- 10 research/exploration sessions
- 10 mixed/general sessions

**By quality** (estimated):
- 15 likely excellent (clean completions, user thanks)
- 20 likely good (normal work)
- 15 likely poor (errors, abandoned, long)

### Selection Script

```python
def select_ground_truth_sessions(target_count: int = 50) -> List[str]:
    """Select diverse sessions for ground truth labeling."""

    all_sessions = langfuse.list_sessions(limit=200)

    # Categorize by size
    small = [s for s in all_sessions if get_trace_count(s) < 10]
    medium = [s for s in all_sessions if 10 <= get_trace_count(s) < 50]
    large = [s for s in all_sessions if get_trace_count(s) >= 50]

    selected = []

    # Sample from each category
    selected.extend(random.sample(small, min(15, len(small))))
    selected.extend(random.sample(medium, min(20, len(medium))))
    selected.extend(random.sample(large, min(15, len(large))))

    return [s.id for s in selected[:target_count]]
```

---

## Labeling Guidelines

### Pre-Labeling Checklist

Before labeling each session:
1. Read the session summary (first and last traces)
2. Identify the apparent goal
3. Note the session size (traces)
4. Check if session appears complete

### Dimension Scoring Guide

#### 1. Context Efficiency (0.0 - 1.0)

| Score | Indicators |
|-------|------------|
| 0.0-0.3 | Multiple reads of same file, loaded many irrelevant files, no targeted searches |
| 0.4-0.6 | Some redundancy, could have been more targeted |
| 0.7-0.8 | Generally efficient, minor redundancy |
| 0.9-1.0 | Perfect - only loaded what was needed, used Glob/Grep first |

**Key questions**:
- Did it read the same file multiple times?
- Did it load files it never used?
- Did it use targeted searches before reading?

#### 2. Instruction Following (poor/partial/good/excellent)

| Score | Indicators |
|-------|------------|
| poor | Ignored explicit instructions, went off-task |
| partial | Followed some instructions, missed key steps |
| good | Followed most instructions with minor deviations |
| excellent | Perfect adherence to all instructions |

**Key questions**:
- Were skill workflow steps followed in order?
- Were user corrections respected?
- Did TodoWrite reflect actual work?

#### 3. Tool Appropriateness (0.0 - 1.0)

| Score | Indicators |
|-------|------------|
| 0.0-0.3 | Used Bash for file ops, many tool failures, wrong tools |
| 0.4-0.6 | Some tool misuse, mostly recovered |
| 0.7-0.8 | Generally correct tools, minor suboptimal choices |
| 0.9-1.0 | Perfect tool selection throughout |

**Key questions**:
- Read instead of cat? Edit instead of sed?
- Were tool failures due to wrong tool choice?
- Did it use specialized tools (Grep, Glob, WebSearch)?

#### 4. Task Completion (failed/partial/complete/exceeded)

| Score | Indicators |
|-------|------------|
| failed | Task not done, major blockers unresolved |
| partial | Some progress, but task incomplete |
| complete | Task finished as requested |
| exceeded | Completed + proactive improvements |

**Key questions**:
- Did the session achieve its goal?
- Were all requested deliverables produced?
- Did the user confirm satisfaction?

#### 5. Error Recovery (poor/slow/adequate/excellent)

| Score | Indicators |
|-------|------------|
| poor | Repeated same error, gave up, didn't understand error |
| slow | Eventually recovered but took many attempts |
| adequate | Recovered reasonably, learned from error |
| excellent | Quick pivot, smart debugging, asked for help when stuck |

**Key questions**:
- If errors occurred, how were they handled?
- Did it repeat the same failing approach?
- Did it try alternative solutions?

#### 6. Cost Efficiency (0.0 - 1.0)

| Score | Indicators |
|-------|------------|
| 0.0-0.3 | Very long for simple task, excessive exploration |
| 0.4-0.6 | Somewhat longer than needed |
| 0.7-0.8 | Reasonable length for complexity |
| 0.9-1.0 | Very efficient, direct path to solution |

**Key questions**:
- Was the trace count reasonable for the task?
- Was there unnecessary back-and-forth?
- Did it take a direct path or meander?

---

## Labeling Workflow

### Step 1: Load Session

```bash
python 03-skills/langfuse/langfuse-get-session/scripts/get_session.py \
  --session-id {session_id}
```

### Step 2: Review Traces

1. Skim all traces for overview
2. Note first user message (intent)
3. Note last traces (completion status)
4. Look for error patterns

### Step 3: Score Each Dimension

Fill out scoring sheet:

```markdown
## Session: {session_id}

**Traces**: {count}
**Apparent Goal**: {description}
**Completion Status**: {complete/incomplete/abandoned}

### Scores

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| context_efficiency | 0.75 | Some redundant file reads in traces 5-8 |
| instruction_following | good | Followed skill workflow, missed one step |
| tool_appropriateness | 0.85 | Good tools, one Bash where Edit would work |
| task_completion | complete | All deliverables produced |
| error_recovery | adequate | Recovered from API error after 2 tries |
| cost_efficiency | 0.70 | Longer than needed, some exploration |

**Overall Quality**: 0.73 (calculated)
```

### Step 4: Store in Langfuse

```bash
python 03-skills/langfuse/langfuse-create-dataset-item/scripts/create_dataset_item.py \
  --dataset "self-improvement-ground-truth" \
  --input '{"session_id": "{session_id}"}' \
  --expected '{"context_efficiency": 0.75, "instruction_following": "good", ...}'
```

---

## Calibration Analysis

### After 50 Sessions Labeled

1. **Run AI scorer on all 50 sessions**
2. **Calculate agreement metrics**:

```python
def calculate_calibration_metrics(
    ai_scores: List[SessionScores],
    human_scores: List[SessionScores]
) -> CalibrationMetrics:

    metrics = {}

    # Numeric dimensions: Pearson correlation, MAE
    for dim in ["context_efficiency", "tool_appropriateness", "cost_efficiency"]:
        ai = [s[dim] for s in ai_scores]
        human = [s[dim] for s in human_scores]

        metrics[dim] = {
            "correlation": pearsonr(ai, human)[0],
            "mae": mean_absolute_error(ai, human),
            "bias": np.mean(ai) - np.mean(human)
        }

    # Categorical dimensions: Cohen's kappa
    for dim in ["instruction_following", "task_completion", "error_recovery"]:
        ai = [s[dim] for s in ai_scores]
        human = [s[dim] for s in human_scores]

        metrics[dim] = {
            "kappa": cohen_kappa_score(ai, human),
            "agreement": accuracy_score(ai, human)
        }

    return metrics
```

3. **Target metrics**:
   - Correlation > 0.8 for numeric dimensions
   - Kappa > 0.6 for categorical dimensions
   - Bias < 0.1 for all dimensions

---

## Success Criteria

- [ ] 50 sessions selected with required diversity
- [ ] Labeling guidelines documented
- [ ] All 50 sessions labeled with rationales
- [ ] Labels stored in ground truth dataset
- [ ] AI-human agreement metrics calculated
- [ ] Calibration findings documented

---

## Risks

| Risk | Mitigation |
|------|------------|
| Labeler fatigue | Spread across 2 weeks, 5-10 per session |
| Inconsistent labeling | Use guidelines, review first 10 for consistency |
| Selection bias | Use stratified sampling script |
| Low agreement | Document disagreements, iterate on guidelines |

---

## Outputs

- 50 labeled sessions in `self-improvement-ground-truth` dataset
- Labeling guidelines in `01-memory/scoring-guidelines.md`
- Calibration report in project outputs
- Recommendations for scorer prompt adjustments

---

*Ready to execute as Project 31*
