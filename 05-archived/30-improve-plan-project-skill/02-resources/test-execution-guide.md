# Test Execution Guide: plan-project Router v2.4

**Project**: 30-improve-plan-project-skill
**Test Suite**: validation-scenarios.yaml
**Total Scenarios**: 35
**Estimated Runtime**: 45 minutes

---

## Test Suite Overview

This comprehensive test suite validates the plan-project router improvements:

| Category | Scenarios | Purpose |
|----------|-----------|---------|
| **P1-P6: Correctness Properties** | 9 | Universal invariants that must ALWAYS hold |
| **TD: Type Detection** | 16 | Semantic matching for all 8 project types |
| **REQ: Requirements** | 4 | Specific functional/non-functional requirements |
| **EDGE: Edge Cases** | 3 | Error handling and boundary conditions |
| **INT: Interactive** | 3 | Full workflows with resume pattern |

---

## Prerequisites

### 1. Langfuse Setup (Optional but recommended)

For trace analysis and automated pass/fail checking:

```bash
# Ensure langfuse-monitor is running
cd 03-skills/langfuse/langfuse-master
python scripts/check_langfuse_config.py --json

# Set environment variable
export LANGFUSE_HOST="http://localhost:3002"
```

### 2. Session Context Cache

Ensure the session context is cached for subagents:

```bash
# This should exist after any normal session
ls 00-system/.cache/session_start_context.xml
```

### 3. Clean Test Environment (Optional)

For isolated testing, use a separate projects folder:

```bash
# Create test projects folder
mkdir -p 02-projects-test/
# Set environment to use test folder (if supported)
```

---

## Execution Modes

### Mode 1: Automated (Non-Interactive Scenarios)

For scenarios that don't require user decisions:

```python
# Example: Run P5_template_structure_all_types
Task(
    prompt="""FIRST: Read 00-system/.cache/session_start_context.xml

    You are testing the template directory structure invariant.

    TASK:
    1. Navigate to: 00-system/skills/projects/plan-project/templates/types/
    2. For EACH of the 8 type folders, verify exactly 5 files exist
    3. List any missing or extra files

    REPORT: [structured report]""",
    subagent_type="general-purpose",
    model="sonnet",
    run_in_background=True
)
```

### Mode 2: Manual (Analyze Existing Sessions)

For analyzing sessions you've already run:

```bash
# Fetch traces by session ID
python 00-system/skills/system/validate-feature/scripts/fetch-traces.py \
    --session-ids "your-session-id" \
    --output traces.json
```

### Mode 3: Interactive (Resume Pattern)

For scenarios requiring user decisions (INT_* scenarios):

```python
# Step 1: Spawn subagent
result = Task(
    prompt="Start plan project for user authentication system...",
    subagent_type="general-purpose"
)
agent_id = result.agent_id

# Step 2: Subagent stops at decision point, reports question
# (e.g., "Which mental models would you like to apply?")

# Step 3: Resume with answer
Task(
    resume=agent_id,
    prompt="User selected: First Principles, Pre-Mortem"
)
```

---

## Test Execution Order

### Phase 1: Static Validation (No project creation)

Run these first - they validate structure without side effects:

1. **P5_template_structure_all_types** - Verify 8 folders × 5 files
2. **P5_template_schema_validation_type_yaml** - Verify _type.yaml schemas
3. **REQ_NF4_ears_in_build_discovery** - Verify EARS in templates
4. **REQ_NF5_correctness_in_build_plan** - Verify Correctness Properties

### Phase 2: Type Detection (Quick, minimal side effects)

Run all TD_* scenarios - they stop after type detection:

1. **TD_build_primary** + **TD_build_synonyms**
2. **TD_integration_primary** + **TD_integration_synonyms**
3. **TD_research_primary** + **TD_research_synonyms**
4. **TD_strategy_primary** + **TD_strategy_synonyms**
5. **TD_content_primary** + **TD_content_synonyms**
6. **TD_process_primary** + **TD_process_synonyms**
7. **TD_skill_primary** + **TD_skill_synonyms**
8. **TD_generic_fallback**

### Phase 3: Property Tests (May create test projects)

1. **P1_router_completeness_clear_intent**
2. **P1_router_completeness_ambiguous_intent**
3. **P6_type_detection_determinism** (5 runs for consistency)

### Phase 4: Workflow Tests (Interactive, creates projects)

1. **P2_discovery_before_mental_models_build**
2. **P3_skill_discovery_integration** (requires add-integration working)
3. **P3_skill_discovery_research** (requires create-research-project working)
4. **P4_resume_context_phase_transitions**

### Phase 5: Requirements and Edge Cases

1. **REQ1_mandatory_router_entry**
2. **REQ3_project_structure_with_type**
3. **EDGE_empty_project_name**
4. **EDGE_special_characters_in_name**
5. **EDGE_project_already_exists**

### Phase 6: Full Workflow Tests (Interactive)

1. **INT_full_build_workflow** - Complete end-to-end
2. **INT_mental_models_mandatory** - Verify MANDATORY enforcement
3. **INT_rediscovery_on_gaps** - Test gap-triggered re-discovery

---

## Running Tests

### Quick Validation (10 minutes)

Run static + type detection tests:

```
# In a new Claude Code session:
1. Load validate-feature skill
2. Run Phase 1 and Phase 2 scenarios
3. Generate report
```

### Full Validation (45 minutes)

Run all phases:

```
# In a new Claude Code session:
1. Load validate-feature skill
2. Run all 35 scenarios in order
3. Use interactive mode for INT_* scenarios
4. Generate comprehensive report
```

### Parallel Execution (Faster but more complex)

Spawn multiple subagents for independent scenarios:

```python
# Run all TD_* tests in parallel (16 scenarios)
agents = []
for scenario in type_detection_scenarios:
    agent = Task(
        prompt=scenario['prompt'],
        subagent_type="general-purpose",
        model="haiku",  # Faster for type detection
        run_in_background=True
    )
    agents.append(agent)

# Wait for completion
time.sleep(60)

# Fetch all traces
python fetch-traces.py --agent-ids "{','.join(a.agent_id for a in agents)}"
```

---

## Expected Results

### Pass Criteria by Category

| Category | Pass Threshold | Rationale |
|----------|----------------|-----------|
| **P1-P6** | 100% | Correctness properties are invariants |
| **TD** | 90% | Semantic matching may vary slightly |
| **REQ** | 100% | Requirements must be met |
| **EDGE** | 80% | Some known issues acceptable |
| **INT** | 100% | Full workflows must complete |

### Known Issues (Expected Failures)

| Scenario | Issue | Status |
|----------|-------|--------|
| P3_skill_discovery_integration | Blocked by Project 36 (scaffold not executed) | EXPECTED FAIL |
| P3_skill_discovery_research | Requires paper-search skill functional | SKIP IF UNAVAILABLE |
| EDGE_project_already_exists | Requires test data setup | SKIP IF NO TEST DATA |

---

## Report Generation

After running tests, generate a validation report:

```markdown
# Validation Report: plan-project Router v2.4

**Date**: 2026-01-07
**Overall Status**: PASS / FAIL / PARTIAL

## Summary by Category

| Category | Passed | Failed | Rate |
|----------|--------|--------|------|
| Correctness Properties | 9/9 | 0 | 100% |
| Type Detection | 14/16 | 2 | 87.5% |
| Requirements | 4/4 | 0 | 100% |
| Edge Cases | 2/3 | 1 | 66.7% |
| Interactive | 3/3 | 0 | 100% |

## Failed Scenarios

### TD_integration_synonyms (Run 3)
- **Input**: "plan project for OAuth flow with Google"
- **Expected**: integration
- **Actual**: build
- **Root Cause**: "OAuth flow" matched build's "implementing functionality"

## Recommendations

1. Improve _type.yaml descriptions for integration type
2. Add "OAuth" and "authentication" to integration keywords
```

---

## Cleanup

After testing, clean up test projects:

```bash
# Remove test projects (if using test folder)
rm -rf 02-projects-test/

# Or archive test projects
mv 02-projects/9*-test-* 05-archived/
```

---

## Troubleshooting

### Issue: Subagent doesn't receive Nexus context

**Solution**: Ensure all prompts start with:
```
FIRST: Read 00-system/.cache/session_start_context.xml
```

### Issue: Langfuse traces not found

**Solution**: Wait longer for ingestion (10-15 seconds after completion)

### Issue: Type detection varies across runs

**Solution**: This may be acceptable - semantic matching has inherent variability. Check if the detected type is semantically reasonable.

### Issue: Interactive test gets stuck

**Solution**: Use resume pattern with explicit answers:
```python
Task(resume=agent_id, prompt="User answered: Build type")
```

---

*Test suite version: 1.0*
*Created: 2026-01-07*
