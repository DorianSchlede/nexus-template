#!/usr/bin/env python3
"""
generate_parent_skill.py - Generate parent SKILL.md (router) for skill-chains

The parent SKILL.md is the CONNECT/ROUTER that:
- Is the ONLY discoverable entry point for the chain
- Routes user intents to appropriate child skills
- Lists all child skills for reference
- Users never need to know internal structure
"""

from typing import Dict, Any, List
from datetime import datetime


def generate_trigger_phrases(config: Dict[str, Any]) -> List[str]:
    """Generate trigger phrases from config."""
    chain_name = config['name']
    phrases = [chain_name.replace('-', ' ')]

    # Add orchestrator-based triggers
    for phase in config.get('phases', []):
        orch = phase['orchestrator']
        phrases.append(orch.replace('-', ' '))

    # Add sub-skill triggers
    for phase in config.get('phases', []):
        for skill in phase.get('sub_skills', []):
            phrases.append(skill.replace('-', ' '))

    return list(set(phrases))


def generate_routing_table(config: Dict[str, Any]) -> str:
    """Generate the routing table markdown."""
    lines = []
    lines.append("| User Intent | Route To |")
    lines.append("|-------------|----------|")

    for phase in config.get('phases', []):
        orch = phase['orchestrator']
        orch_display = orch.replace('-', ' ')
        phase_name = phase.get('name', f'phase {phase}')

        # Orchestrator routes
        intents = [
            f'"{orch_display}"',
            f'"start {phase_name}"',
            f'"run {phase_name}"',
        ]
        lines.append(f"| {', '.join(intents)} | `orchestrators/{orch}/SKILL.md` |")

    # Sub-skill direct routes
    for phase in config.get('phases', []):
        for skill in phase.get('sub_skills', []):
            skill_display = skill.replace('-', ' ')
            lines.append(f'| "{skill_display}" | `skills/{skill}/SKILL.md` |')

    return '\n'.join(lines)


def generate_skill_inventory(config: Dict[str, Any]) -> str:
    """Generate skill inventory tables."""
    lines = []

    # Orchestrators
    lines.append("### Orchestrators (User-Facing Entry Points)")
    lines.append("")
    lines.append("| Skill | Phase | Purpose |")
    lines.append("|-------|-------|---------|")

    for i, phase in enumerate(config.get('phases', []), 1):
        orch = phase['orchestrator']
        desc = phase.get('description', f'Phase {i}: {phase.get("name", "unnamed")}')
        lines.append(f"| [{orch}](orchestrators/{orch}/SKILL.md) | {i} | {desc} |")

    lines.append("")

    # Sub-skills
    lines.append("### Sub-Skills (Called by Orchestrators)")
    lines.append("")
    lines.append("| Skill | Purpose | Called By |")
    lines.append("|-------|---------|-----------|")

    for phase in config.get('phases', []):
        orch = phase['orchestrator']
        for skill in phase.get('sub_skills', []):
            lines.append(f"| [{skill}](skills/{skill}/SKILL.md) | TODO | {orch} |")

    # Shared methodologies
    if config.get('shared_skills'):
        lines.append("")
        lines.append("### Shared Methodologies (DO NOT LOAD DIRECTLY)")
        lines.append("")
        lines.append("| Skill | Purpose |")
        lines.append("|-------|---------|")

        for shared in config.get('shared_skills', []):
            lines.append(f"| [{shared}](shared/{shared}/SKILL.md) | Loaded by subagents |")

    return '\n'.join(lines)


def generate_pipeline_flow(config: Dict[str, Any]) -> str:
    """Generate pipeline flow diagram."""
    lines = []
    lines.append("```")

    for i, phase in enumerate(config.get('phases', []), 1):
        phase_name = phase.get('name', f'Phase {i}')
        orch = phase['orchestrator']
        sub_skills = phase.get('sub_skills', [])

        lines.append(f"Phase {i}: {phase_name.title()} ({orch})")

        for j, skill in enumerate(sub_skills):
            prefix = "├──" if j < len(sub_skills) - 1 else "└──"
            lines.append(f"{prefix} {skill}")

        if phase.get('gate'):
            gate_name = phase['gate'].get('name', f'PHASE_{i}_COMPLETE')
            lines.append(f"└── Gate: {gate_name.upper()}")

        lines.append("")

    lines.append("```")
    return '\n'.join(lines)


def generate_parent_skill(config: Dict[str, Any]) -> str:
    """
    Generate parent SKILL.md content.

    Args:
        config: Chain configuration

    Returns:
        Markdown content for parent SKILL.md
    """
    chain_name = config['name']
    description = config.get('description', f'{chain_name} skill-chain')
    trigger_phrases = generate_trigger_phrases(config)

    # Build YAML frontmatter
    triggers_str = "', '".join(trigger_phrases)

    content = f"""---
name: {chain_name}
description: "{description}. Load when user mentions '{triggers_str}'. This is the MASTER entry point - routes to appropriate child skills."
type: skill-chain
version: "1.0"
---

# {chain_name.replace('-', ' ').title()}

{description}

**This is a CONNECT/ROUTER skill** - like `beam-connect`, it routes to specialized skills.

## How It Works

1. **User talks to this skill** (the parent)
2. **This skill routes to the appropriate child** based on intent
3. **User never needs to know the internal structure**

## Quick Start

| What You Want | Say This |
|--------------|----------|
"""

    # Add quick start examples
    for phase in config.get('phases', []):
        orch = phase['orchestrator']
        orch_display = orch.replace('-', ' ')
        content += f'| {phase.get("name", "Run phase").title()} | "{orch_display}" |\n'

    content += f"""
## Routing Table

Based on user intent, **load the appropriate child skill**:

{generate_routing_table(config)}

"""

    # Add shared methodology warning if applicable
    if config.get('shared_skills'):
        shared_names = ', '.join([f'`shared/{s}/`' for s in config['shared_skills']])
        content += f"""**DO NOT load {shared_names} directly** - they're loaded by subagents.

"""

    content += f"""## Chain Documentation

- **Contract**: See `_chain.yaml` for validation contract
- **Documentation**: See `_index.md` for auto-generated docs with Mermaid diagrams

## Skill Inventory

{generate_skill_inventory(config)}

## Pipeline Flow

{generate_pipeline_flow(config)}

---

**Version**: 1.0 ({datetime.now().strftime('%Y-%m-%d')})
**Architecture**: Nested skill-chain
"""

    return content


if __name__ == '__main__':
    # Example usage
    example_config = {
        'name': 'interview-analysis',
        'description': 'Analyze interview transcripts for themes and insights',
        'phases': [
            {
                'name': 'preparation',
                'description': 'Import and preprocess transcripts',
                'orchestrator': 'prepare-interview-project',
                'sub_skills': ['transcript-import', 'transcript-preprocess'],
                'gate': {'name': 'readiness-gate'},
            },
            {
                'name': 'analysis',
                'description': 'Analyze transcripts and synthesize themes',
                'orchestrator': 'execute-interview-analysis',
                'sub_skills': ['transcript-analyze', 'theme-synthesize'],
            },
        ],
        'shared_skills': ['transcript-analyze-core'],
    }

    print(generate_parent_skill(example_config))
