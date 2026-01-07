# Project 35: Discovery

**Date**: 2026-01-07
**Source**: Project 27 research findings + skill investigation

---

## Questions & Answers

### Q1: What score configs do we need to create?

**Answer**: 7 configs based on validated scoring dimensions from Project 27:

| Config Name | Type | Parameters | Description |
|-------------|------|------------|-------------|
| `task_completion` | CATEGORICAL | failed(0), partial(1), complete(2), exceeded(3) | Did it achieve the goal? |
| `execution_quality` | NUMERIC | min=0, max=1 | How well were instructions followed? |
| `tool_mastery` | NUMERIC | min=0, max=1 | Tool selection + error recovery |
| `resource_efficiency` | NUMERIC | min=0, max=1 | Context/token efficiency |
| `security_compliance` | CATEGORICAL | violation(0), risk(1), compliant(2), exemplary(3) | Security practices |
| `user_satisfaction` | CATEGORICAL | frustrated(0), neutral(1), satisfied(2), delighted(3) | User response signals |
| `overall_quality` | NUMERIC | min=0, max=1 | Weighted aggregate |

---

### Q2: What skills do we use?

**Answer**: Langfuse skills are ready:

| Task | Skill | Script |
|------|-------|--------|
| List existing configs | `langfuse-list-score-configs` | `scripts/list_score_configs.py` |
| Create new config | `langfuse-create-score-config` | `scripts/create_score_config.py` |
| Create dataset | `langfuse-create-dataset` | `scripts/create_dataset.py` |
| Create test score | `langfuse-create-score` | `scripts/create_score.py` |

**CLI patterns**:
```bash
# NUMERIC config
python scripts/create_score_config.py \
  --name "execution_quality" \
  --data-type NUMERIC \
  --min 0 --max 1 \
  --description "How well instructions were followed"

# CATEGORICAL config
python scripts/create_score_config.py \
  --name "task_completion" \
  --data-type CATEGORICAL \
  --categories "failed,partial,complete,exceeded" \
  --description "Task completion status"
```

---

### Q3: Do any score configs already exist?

**Answer**: From Project 27 testing, 2 test configs exist:
- `test-efficiency` (NUMERIC)
- `test-quality` (CATEGORICAL)

**Action**: Verify current state at execution time, clean up test configs if needed.

---

### Q4: What dataset do we need?

**Answer**: 1 dataset for ground truth labels:
- Name: `self-improvement-ground-truth`
- Description: "Human-labeled sessions for scorer calibration"
- Purpose: Store manual labels for AI-human agreement calibration (Project 38)

**Note**: A `test-ground-truth` dataset may exist from Project 27 testing.

---

### Q5: How do we test scoring works?

**Answer**: Create test scores on existing traces:

1. Get a trace ID from an existing session
2. Create score with each config
3. Verify scores visible in Langfuse UI

**From API validation**:
- Trace-level scoring: works
- Observation-level scoring: works
- CATEGORICAL values: use integers (0, 1, 2, 3)
- Comments supported for rationale

---

### Q6: Any API quirks to handle?

**Answer**: Yes, from Project 27 validation:

1. **Annotation queues fail** (400 Bad Request)
   - Don't use for this project
   - Use Datasets API instead

2. **CATEGORICAL values are integers**
   - API accepts integer, returns label in UI
   - Example: `value=2` → displays as "complete"

3. **Config ID needed for typed scores**
   - Creating score without config_id works but loses validation
   - Always use config_id for consistency

4. **Can't update score config name**
   - If wrong name, must delete and recreate
   - Create carefully

---

## Tools Available

### Working Scripts (verified in Project 27)

| Path | Purpose |
|------|---------|
| `03-skills/langfuse/langfuse-list-score-configs/scripts/list_score_configs.py` | List existing configs |
| `03-skills/langfuse/langfuse-create-score-config/scripts/create_score_config.py` | Create new config |
| `03-skills/langfuse/langfuse-create-dataset/scripts/create_dataset.py` | Create dataset |
| `03-skills/langfuse/langfuse-create-score/scripts/create_score.py` | Create scores |
| `03-skills/langfuse/langfuse-list-sessions/scripts/list_sessions.py` | Find test sessions |
| `03-skills/langfuse/langfuse-list-traces/scripts/list_traces.py` | Find trace IDs |

### Langfuse Connection

- Host: `localhost:3002`
- Client: `langfuse_client.py` in `langfuse-master/scripts/`
- Auth: Environment variables (already configured)

---

## Risk Assessment

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Langfuse not running | Low | Check before starting |
| Duplicate config names | Low | List first, handle duplicates |
| Wrong config structure | Medium | Test one config before bulk creation |
| Test data pollution | Low | Use clear naming, clean up test configs |

---

## Open Questions

1. **Should we delete the test configs from Project 27?**
   - Recommendation: Yes, for clean state

2. **Should we delete the test dataset?**
   - Recommendation: No harm keeping it, but create production dataset fresh

---

## Ready for Planning

All discovery complete. We have:
- Clear list of 7 configs to create
- Working scripts verified
- API quirks documented
- Test strategy defined

*Next: Create 03-plan.md with execution strategy*
