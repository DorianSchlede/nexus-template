#!/usr/bin/env python3
"""
generate_orchestrator.py - Generate orchestrator SKILL.md files

Orchestrators are user-facing entry points for each phase.
They coordinate sub-skills and manage the workflow for their phase.
"""

from typing import Dict, Any
from datetime import datetime


def generate_orchestrator(config: Dict[str, Any], phase: Dict[str, Any]) -> str:
    """
    Generate orchestrator SKILL.md content.

    Args:
        config: Full chain configuration
        phase: Phase configuration for this orchestrator

    Returns:
        Markdown content for orchestrator SKILL.md
    """
    chain_name = config['name']
    orch_name = phase['orchestrator']
    phase_name = phase.get('name', 'unnamed')
    phase_num = config.get('phases', []).index(phase) + 1
    description = phase.get('description', f'Phase {phase_num} orchestrator for {chain_name}')
    sub_skills = phase.get('sub_skills', [])

    # Build trigger phrases
    triggers = [
        orch_name.replace('-', ' '),
        f'run {phase_name}',
        f'start {phase_name}',
        f'phase {phase_num}',
    ]
    triggers_str = "', '".join(triggers)

    content = f"""---
name: {orch_name}
description: "{description}. Load when user mentions '{triggers_str}'."
type: orchestrator
version: "1.0"
parent_chain: {chain_name}
phase: {phase_num}
---

# {orch_name.replace('-', ' ').title()}

**Phase {phase_num}**: {phase_name.title()} orchestrator for [{chain_name}](../../SKILL.md).

## Purpose

{description}

## Sub-Skills Used

This orchestrator coordinates the following sub-skills:

| Sub-Skill | Purpose |
|-----------|---------|
"""

    for skill in sub_skills:
        content += f"| [{skill}](../../skills/{skill}/SKILL.md) | TODO: Add description |\n"

    content += f"""
## Workflow

<!-- TODO: Define the step-by-step workflow -->

### Step 1: Initialize

```
- Create TodoWrite with workflow steps
- Validate prerequisites
- Set up working context
```

### Step 2: Execute Sub-Skills

"""

    for i, skill in enumerate(sub_skills, 1):
        content += f"""#### {i}. {skill.replace('-', ' ').title()}

```
- Load skill: skills/{skill}/SKILL.md
- Input: TODO
- Output: TODO
```

"""

    # Add gate section if defined
    if phase.get('gate'):
        gate = phase['gate']
        gate_name = gate.get('name', f'phase-{phase_num}-gate')
        conditions = gate.get('conditions', [])

        content += f"""### Step {len(sub_skills) + 2}: Verify Gate Conditions

**Gate: {gate_name}**

Before proceeding to the next phase, verify:

"""
        for condition in conditions:
            content += f"- [ ] {condition}\n"

        content += "\n"

    # Add outputs section if defined
    if phase.get('outputs'):
        content += """## Outputs

This phase produces the following outputs:

| Output | Location | Required |
|--------|----------|----------|
"""
        for output in phase['outputs']:
            required = "Yes" if output.get('required', True) else "No"
            content += f"| {output['path'].split('/')[-1]} | `{output['path']}` | {required} |\n"

        content += "\n"

    content += f"""## Error Handling

<!-- TODO: Define error handling for this orchestrator -->

- If a sub-skill fails: ...
- If gate conditions not met: ...
- Recovery procedures: ...

## Usage Example

```
User: "{orch_name.replace('-', ' ')}"
→ This skill is loaded
→ Executes workflow steps 1-N
→ Produces outputs
→ Verifies gate conditions
```

---

**Parent Chain**: [{chain_name}](../../SKILL.md)
**Version**: 1.0 ({datetime.now().strftime('%Y-%m-%d')})
"""

    return content


if __name__ == '__main__':
    # Example usage
    example_config = {
        'name': 'interview-analysis',
        'phases': [
            {
                'name': 'preparation',
                'description': 'Import and preprocess interview transcripts',
                'orchestrator': 'prepare-interview-project',
                'sub_skills': ['transcript-import', 'transcript-preprocess'],
                'outputs': [
                    {'path': '02-resources/_briefing.md', 'required': True},
                    {'path': '02-resources/transcripts/*/_metadata.json', 'required': True},
                ],
                'gate': {
                    'name': 'readiness-gate',
                    'conditions': ['transcripts_preprocessed > 0', '_briefing.md exists'],
                },
            },
        ],
    }

    print(generate_orchestrator(example_config, example_config['phases'][0]))
