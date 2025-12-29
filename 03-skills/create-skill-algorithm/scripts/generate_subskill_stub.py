#!/usr/bin/env python3
"""
generate_subskill_stub.py - Generate sub-skill SKILL.md stubs

Sub-skills are called by orchestrators, not directly by users.
These stubs provide a starting template that needs to be filled in.
"""

from typing import Dict, Any
from datetime import datetime


def generate_subskill_stub(config: Dict[str, Any], skill_name: str, phase: Dict[str, Any]) -> str:
    """
    Generate sub-skill SKILL.md stub content.

    Args:
        config: Full chain configuration
        skill_name: Name of this sub-skill
        phase: Phase configuration that contains this sub-skill

    Returns:
        Markdown content for sub-skill SKILL.md
    """
    chain_name = config['name']
    orch_name = phase['orchestrator']
    phase_name = phase.get('name', 'unnamed')
    phase_num = config.get('phases', []).index(phase) + 1

    # Try to infer purpose from name
    name_parts = skill_name.replace('-', ' ').split()
    inferred_action = name_parts[0] if name_parts else 'process'
    inferred_subject = ' '.join(name_parts[1:]) if len(name_parts) > 1 else 'data'

    content = f"""---
name: {skill_name}
description: "TODO: Add description. Load when orchestrator calls this skill."
type: sub-skill
version: "1.0"
parent_chain: {chain_name}
called_by: {orch_name}
---

# {skill_name.replace('-', ' ').title()}

**Sub-skill** for [{chain_name}](../../SKILL.md) → Phase {phase_num}: {phase_name}.

Called by: [{orch_name}](../../orchestrators/{orch_name}/SKILL.md)

## Purpose

<!-- TODO: Describe what this skill does -->

This skill {inferred_action}s {inferred_subject} as part of the {phase_name} phase.

## Inputs

<!-- TODO: Define inputs -->

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| TODO | string | Yes | Description |

## Outputs

<!-- TODO: Define outputs -->

| Output | Location | Description |
|--------|----------|-------------|
| TODO | `path/to/output` | Description |

## Workflow

<!-- TODO: Define the workflow steps -->

### Step 1: Validate Inputs

```
- Check required inputs exist
- Validate input format
```

### Step 2: Process

```
- Main processing logic
- TODO: Add specific steps
```

### Step 3: Generate Output

```
- Create output files
- Validate output format
```

## Implementation Notes

<!-- TODO: Add implementation details -->

- Dependencies: None
- Scripts: `scripts/` (if applicable)
- References: `references/` (if applicable)

## Error Handling

<!-- TODO: Define error handling -->

| Error | Cause | Resolution |
|-------|-------|------------|
| TODO | Cause | How to fix |

## Usage

This skill is called by the orchestrator, not directly:

```
# In orchestrator workflow:
# Step N: Load skills/{skill_name}/SKILL.md
# Execute with: [inputs]
# Produces: [outputs]
```

---

**Parent Chain**: [{chain_name}](../../SKILL.md)
**Orchestrator**: [{orch_name}](../../orchestrators/{orch_name}/SKILL.md)
**Version**: 1.0 ({datetime.now().strftime('%Y-%m-%d')})
**Status**: STUB - Needs implementation
"""

    return content


if __name__ == '__main__':
    # Example usage
    example_config = {
        'name': 'interview-analysis',
        'phases': [
            {
                'name': 'preparation',
                'orchestrator': 'prepare-interview-project',
                'sub_skills': ['transcript-import', 'transcript-preprocess'],
            },
        ],
    }

    print(generate_subskill_stub(
        example_config,
        'transcript-import',
        example_config['phases'][0]
    ))
