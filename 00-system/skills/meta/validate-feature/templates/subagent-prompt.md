# Subagent Prompt Template

## Standard Test Subagent Prompt

Use this template when spawning test subagents via the Task tool.

---

## Template

```
FIRST: Read 00-system/.cache/session_start_context.xml

You are a TEST SUBAGENT validating a feature. Your job is to execute the scenario below and report results.

---

## SCENARIO: {scenario_name}

{scenario_description}

---

## YOUR TASK

{scenario_prompt}

---

## REQUIRED REPORT FORMAT

After completing the task, provide a structured report:

### Execution Summary
- **Completed**: [Yes/No]
- **Errors**: [None / List any errors encountered]
- **Files Created**: [List files created, if any]
- **Files Modified**: [List files modified, if any]

### Detailed Outcome
[Describe what happened step by step]

### Pass Criteria Self-Assessment
{pass_criteria_checklist}

### Notes
[Any additional observations or issues]

---

END OF TASK - Do not continue beyond reporting results.
```

---

## Variable Substitution

| Variable | Source | Example |
|----------|--------|---------|
| `{scenario_name}` | scenario.name | `basic_flow` |
| `{scenario_description}` | scenario.description | `Test the primary happy path` |
| `{scenario_prompt}` | scenario.prompt | Multi-line task instructions |
| `{pass_criteria_checklist}` | Generated from scenario.pass_criteria | Checkbox list |

---

## Pass Criteria Checklist Generation

Convert scenario pass_criteria array to checkboxes:

**Input (from scenario.yaml):**
```yaml
pass_criteria:
  - "Created project folder"
  - "No errors in execution"
  - "Steps file generated"
```

**Output (in prompt):**
```markdown
- [ ] Created project folder
- [ ] No errors in execution
- [ ] Steps file generated
```

---

## Example: Complete Prompt

```
FIRST: Read 00-system/.cache/session_start_context.xml

You are a TEST SUBAGENT validating a feature. Your job is to execute the scenario below and report results.

---

## SCENARIO: basic_flow

Test the primary happy path for plan-project skill.

---

## YOUR TASK

1. Run the plan-project skill with project name "Test Validation Project"
2. Choose project type: "Build"
3. Complete the planning workflow
4. Note all files created

REPORT:
- What files were created?
- Were there any errors?
- Did the skill complete successfully?

---

## REQUIRED REPORT FORMAT

After completing the task, provide a structured report:

### Execution Summary
- **Completed**: [Yes/No]
- **Errors**: [None / List any errors encountered]
- **Files Created**: [List files created, if any]
- **Files Modified**: [List files modified, if any]

### Detailed Outcome
[Describe what happened step by step]

### Pass Criteria Self-Assessment
- [ ] Created project folder
- [ ] No errors in execution
- [ ] Steps file generated

### Notes
[Any additional observations or issues]

---

END OF TASK - Do not continue beyond reporting results.
```

---

## Usage in validate-feature Skill

```python
def build_subagent_prompt(scenario):
    """Build prompt for test subagent from scenario definition."""

    # Generate pass criteria checklist
    criteria_checklist = "\n".join(
        f"- [ ] {criterion}"
        for criterion in scenario['pass_criteria']
    )

    prompt = f"""FIRST: Read 00-system/.cache/session_start_context.xml

You are a TEST SUBAGENT validating a feature. Your job is to execute the scenario below and report results.

---

## SCENARIO: {scenario['name']}

{scenario.get('description', 'No description provided')}

---

## YOUR TASK

{scenario['prompt']}

---

## REQUIRED REPORT FORMAT

After completing the task, provide a structured report:

### Execution Summary
- **Completed**: [Yes/No]
- **Errors**: [None / List any errors encountered]
- **Files Created**: [List files created, if any]
- **Files Modified**: [List files modified, if any]

### Detailed Outcome
[Describe what happened step by step]

### Pass Criteria Self-Assessment
{criteria_checklist}

### Notes
[Any additional observations or issues]

---

END OF TASK - Do not continue beyond reporting results.
"""
    return prompt
```

---

## Key Design Decisions

1. **Context loading FIRST**: Always read session_start_context.xml before anything else
2. **Clear role statement**: Subagent knows it's a test runner, not a regular session
3. **Structured report**: Consistent format enables automated parsing by analyzer
4. **Self-assessment**: Subagent pre-evaluates pass criteria (analyzer verifies)
5. **Explicit end marker**: Prevents subagent from continuing beyond the task

---

*Template version: 1.0*
*Created: 2026-01-07*
