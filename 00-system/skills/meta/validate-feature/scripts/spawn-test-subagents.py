#!/usr/bin/env python3
"""
Spawn Test Subagents for Feature Validation

This script is NOT executed directly - it documents the pattern for Claude
to spawn test subagents using the Task tool.

The actual spawning happens through Claude Code's Task tool in parallel.
"""

import yaml
from pathlib import Path
from typing import List, Dict, Any


def load_scenarios(project_path: str) -> List[Dict[str, Any]]:
    """Load validation scenarios from project's validation-scenarios.yaml."""
    scenarios_path = Path(project_path) / "02-resources" / "validation-scenarios.yaml"

    if not scenarios_path.exists():
        raise FileNotFoundError(f"No scenarios file at {scenarios_path}")

    with open(scenarios_path, 'r') as f:
        data = yaml.safe_load(f)

    return data.get('scenarios', [])


def build_subagent_prompt(scenario: Dict[str, Any]) -> str:
    """Build prompt for test subagent from scenario definition."""

    # Generate pass criteria checklist
    criteria_checklist = "\n".join(
        f"- [ ] {criterion}"
        for criterion in scenario.get('pass_criteria', [])
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


def generate_task_tool_calls(scenarios: List[Dict[str, Any]]) -> str:
    """
    Generate the Task tool call pattern for Claude to execute.

    Claude should use the Task tool with:
    - subagent_type: "general-purpose"
    - model: "sonnet" (for proper simulation)
    - run_in_background: true (for parallel execution)
    - prompt: built from scenario

    Returns documentation string showing the pattern.
    """

    output = []
    output.append("## Task Tool Calls for Parallel Subagent Spawning\n")
    output.append("Execute these Task tool calls IN PARALLEL (single message, multiple tool uses):\n")

    for scenario in scenarios:
        runs = scenario.get('runs', 5)
        prompt = build_subagent_prompt(scenario)

        for i in range(1, runs + 1):
            output.append(f"""
### {scenario['name']} - Run {i}/{runs}

```
Task tool:
  subagent_type: "general-purpose"
  model: "sonnet"
  run_in_background: true
  description: "Test {scenario['name']} run {i}"
  prompt: |
{indent_text(prompt, 4)}
```
""")

    return "\n".join(output)


def indent_text(text: str, spaces: int) -> str:
    """Indent each line of text by specified spaces."""
    indent = " " * spaces
    return "\n".join(indent + line for line in text.split("\n"))


# Pattern for collecting agent IDs from Task tool responses
AGENT_ID_COLLECTION_PATTERN = """
## Collecting Agent IDs

After spawning subagents, Claude receives responses containing agent IDs.

### Response Format
Each Task tool response includes:
```
Agent ID: {agent_id}
```

### Collection Pattern
```python
agent_ids = []
for response in task_responses:
    # Extract agent ID from response
    # Format: 7-character hex string (e.g., "ac75a88")
    agent_id = extract_agent_id(response)
    agent_ids.append(agent_id)
```

### Composite Key Generation
For each agent_id, generate composite key for trace retrieval:
```python
composite_keys = []
for agent_id in agent_ids:
    # Will be populated after querying Langfuse
    # Format: "{session_id}:{agent_id}"
    composite_keys.append({
        'agent_id': agent_id,
        'conversation_id': f"agent-{agent_id}",
        'session_id': None  # Populated from Langfuse
    })
```
"""


if __name__ == "__main__":
    # Example usage - demonstrates the pattern
    sample_scenario = {
        'name': 'basic_flow',
        'description': 'Test basic skill execution',
        'prompt': '''Run the plan-project skill with:
- Project name: "Test Validation"
- Project type: "Build"

Complete the planning workflow and report what files were created.''',
        'pass_criteria': [
            'Created project folder',
            'No errors in execution',
            'Steps file generated'
        ],
        'runs': 3
    }

    print("Sample subagent prompt:")
    print("=" * 60)
    print(build_subagent_prompt(sample_scenario))
    print("\n" + "=" * 60)
    print("\nAgent ID collection pattern:")
    print(AGENT_ID_COLLECTION_PATTERN)
