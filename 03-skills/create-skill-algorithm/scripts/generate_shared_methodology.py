#!/usr/bin/env python3
"""
generate_shared_methodology.py - Generate shared methodology SKILL.md files

Shared methodologies are skills loaded by subagents, NEVER directly.
They contain reusable analysis/processing methodologies.
"""

from typing import Dict, Any
from datetime import datetime


def generate_shared_methodology(config: Dict[str, Any], shared_name: str) -> str:
    """
    Generate shared methodology SKILL.md content.

    Args:
        config: Full chain configuration
        shared_name: Name of this shared methodology

    Returns:
        Markdown content for shared methodology SKILL.md
    """
    chain_name = config['name']

    # Try to infer what it does from name
    name_parts = shared_name.replace('-', ' ').split()
    if 'core' in name_parts:
        name_parts.remove('core')
    inferred_purpose = ' '.join(name_parts)

    content = f"""---
name: {shared_name}
description: "Shared methodology for {inferred_purpose}. DO NOT LOAD DIRECTLY - loaded by subagents."
type: shared-methodology
version: "1.0"
parent_chain: {chain_name}
---

# {shared_name.replace('-', ' ').title()}

## ⚠️ DO NOT LOAD DIRECTLY

This is a **shared methodology** - it is loaded by subagents spawned by orchestrators.

**If you reached this skill directly, you probably meant to use one of:**
- [{chain_name}](../../SKILL.md) (main entry point)

## Purpose

<!-- TODO: Describe the methodology -->

This methodology provides reusable {inferred_purpose} logic for subagents.

## When This Is Loaded

This methodology is loaded by subagents when:
- TODO: Describe the scenarios

## Methodology

<!-- TODO: Define the step-by-step methodology -->

### 1. Initialize Context

```
- Receive context from parent agent
- Validate required inputs
- Set up processing state
```

### 2. Core Processing

```
- Main methodology steps
- TODO: Add specific steps
```

### 3. Return Results

```
- Package results for parent
- Include verification data
- Return to spawning agent
```

## Input Contract

<!-- TODO: Define what the subagent receives -->

The subagent receives:

| Field | Type | Description |
|-------|------|-------------|
| TODO | string | Description |

## Output Contract

<!-- TODO: Define what the subagent returns -->

The subagent returns:

| Field | Type | Description |
|-------|------|-------------|
| TODO | string | Description |

## Quality Assurance

<!-- TODO: Add quality checks -->

This methodology includes:
- Validation checks: TODO
- Evidence requirements: TODO
- Error handling: TODO

## Implementation Notes

<!-- TODO: Add implementation details -->

- This skill defines WHAT to do, not HOW to trigger it
- Subagents load this to inherit the methodology
- All processing happens within the subagent context

---

**Parent Chain**: [{chain_name}](../../SKILL.md)
**Type**: Shared Methodology (DO NOT LOAD DIRECTLY)
**Version**: 1.0 ({datetime.now().strftime('%Y-%m-%d')})
**Status**: STUB - Needs implementation
"""

    return content


if __name__ == '__main__':
    # Example usage
    example_config = {
        'name': 'interview-analysis',
        'shared_skills': ['transcript-analyze-core'],
    }

    print(generate_shared_methodology(example_config, 'transcript-analyze-core'))
