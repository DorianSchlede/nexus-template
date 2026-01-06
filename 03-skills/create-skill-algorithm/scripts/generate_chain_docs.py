#!/usr/bin/env python3
"""
generate_chain_docs.py - Generate _index.md documentation with Mermaid diagrams

Creates auto-generated documentation for skill-chains including:
- Architecture diagram (Mermaid)
- Process flow diagram (Mermaid sequence)
- Skill inventory tables
- Output mappings
- Usage examples
"""

from typing import Dict, Any, List
from datetime import datetime


def generate_architecture_diagram(config: Dict[str, Any]) -> str:
    """Generate Mermaid architecture diagram."""
    chain_name = config['name']
    lines = []
    lines.append("```mermaid")
    lines.append("graph TB")
    lines.append(f'    subgraph "{chain_name.replace("-", " ").title()} Skill-Chain"')
    lines.append('        PARENT[SKILL.md<br/>Parent Router]')
    lines.append('')

    # Orchestrators subgraph
    lines.append('        subgraph "orchestrators/"')
    for i, phase in enumerate(config.get('phases', []), 1):
        orch = phase['orchestrator']
        orch_id = orch.replace('-', '_').upper()
        phase_name = phase.get('name', f'Phase {i}')
        lines.append(f'            {orch_id}[{orch}<br/>Phase {i}: {phase_name.title()}]')
    lines.append('        end')
    lines.append('')

    # Skills subgraph
    all_subskills = []
    for phase in config.get('phases', []):
        all_subskills.extend(phase.get('sub_skills', []))

    if all_subskills:
        lines.append('        subgraph "skills/"')
        for skill in all_subskills:
            skill_id = skill.replace('-', '_').upper()
            lines.append(f'            {skill_id}[{skill}]')
        lines.append('        end')
        lines.append('')

    # Shared subgraph
    if config.get('shared_skills'):
        lines.append('        subgraph "shared/"')
        for shared in config.get('shared_skills', []):
            shared_id = shared.replace('-', '_').upper()
            lines.append(f'            {shared_id}[{shared}<br/>DO NOT LOAD DIRECTLY]')
        lines.append('        end')
        lines.append('')

    # Validation subgraph
    lines.append('        subgraph "validation/"')
    lines.append('            VA[validate_*.py]')
    lines.append('        end')
    lines.append('    end')
    lines.append('')

    # Connections from parent to orchestrators
    for phase in config.get('phases', []):
        orch = phase['orchestrator']
        orch_id = orch.replace('-', '_').upper()
        lines.append(f'    PARENT --> {orch_id}')

    # Connections from orchestrators to sub-skills
    for phase in config.get('phases', []):
        orch = phase['orchestrator']
        orch_id = orch.replace('-', '_').upper()
        for skill in phase.get('sub_skills', []):
            skill_id = skill.replace('-', '_').upper()
            lines.append(f'    {orch_id} --> {skill_id}')

    # Connections to shared (dotted lines)
    if config.get('shared_skills'):
        for shared in config.get('shared_skills', []):
            shared_id = shared.replace('-', '_').upper()
            # Connect from related skills (guess based on name similarity)
            for phase in config.get('phases', []):
                for skill in phase.get('sub_skills', []):
                    # Check if skill name is similar to shared
                    base_shared = shared.replace('-core', '').replace('-', '')
                    base_skill = skill.replace('-', '')
                    if base_shared in base_skill or base_skill in base_shared:
                        skill_id = skill.replace('-', '_').upper()
                        lines.append(f'    {skill_id} -.-> {shared_id}')
                        break

    lines.append("```")
    return '\n'.join(lines)


def generate_sequence_diagram(config: Dict[str, Any]) -> str:
    """Generate Mermaid sequence diagram for process flow."""
    lines = []
    lines.append("```mermaid")
    lines.append("sequenceDiagram")

    # Define participants
    lines.append("    participant U as User")

    for phase in config.get('phases', []):
        orch = phase['orchestrator']
        orch_short = ''.join([p[0].upper() for p in orch.split('-')])
        lines.append(f"    participant {orch_short} as {orch}")

    # Add sub-skills as participants (only show unique ones used)
    shown_skills = set()
    for phase in config.get('phases', []):
        for skill in phase.get('sub_skills', []):
            if skill not in shown_skills:
                skill_short = ''.join([p[0].upper() for p in skill.split('-')])
                lines.append(f"    participant {skill_short} as {skill}")
                shown_skills.add(skill)

    if config.get('shared_skills'):
        for shared in config['shared_skills']:
            shared_short = ''.join([p[0].upper() for p in shared.split('-')])
            lines.append(f"    participant {shared_short} as {shared}")

    lines.append("")

    # Generate interactions
    for i, phase in enumerate(config.get('phases', []), 1):
        orch = phase['orchestrator']
        orch_short = ''.join([p[0].upper() for p in orch.split('-')])
        phase_name = phase.get('name', f'Phase {i}')

        lines.append(f"    U->>{orch_short}: Start {phase_name}")

        for skill in phase.get('sub_skills', []):
            skill_short = ''.join([p[0].upper() for p in skill.split('-')])
            lines.append(f"    {orch_short}->>{skill_short}: Execute")
            lines.append(f"    {skill_short}-->>{orch_short}: Results")

        # Show gate if defined
        if phase.get('gate'):
            gate_name = phase['gate'].get('name', f'phase-{i}-gate')
            lines.append(f"    Note over {orch_short}: Gate: {gate_name}")

        lines.append("")

    lines.append("```")
    return '\n'.join(lines)


def generate_skill_inventory(config: Dict[str, Any]) -> str:
    """Generate skill inventory tables."""
    lines = []

    # Orchestrators table
    lines.append("### Orchestrators (User Entry Points)")
    lines.append("")
    lines.append("| Skill | Path | Purpose |")
    lines.append("|-------|------|---------|")

    for i, phase in enumerate(config.get('phases', []), 1):
        orch = phase['orchestrator']
        desc = phase.get('description', f'Phase {i}: {phase.get("name", "unnamed")}')
        lines.append(f"| {orch} | `orchestrators/{orch}/` | {desc} |")

    lines.append("")

    # Sub-skills table
    lines.append("### Sub-Skills")
    lines.append("")
    lines.append("| Skill | Path | Purpose |")
    lines.append("|-------|------|---------|")

    for phase in config.get('phases', []):
        for skill in phase.get('sub_skills', []):
            lines.append(f"| {skill} | `skills/{skill}/` | TODO |")

    lines.append("")

    # Shared methodologies table
    if config.get('shared_skills'):
        lines.append("### Shared Methodologies")
        lines.append("")
        lines.append("| Skill | Path | Note |")
        lines.append("|-------|------|------|")

        for shared in config['shared_skills']:
            lines.append(f"| {shared} | `shared/{shared}/` | **DO NOT LOAD DIRECTLY** - Loaded by subagents |")

        lines.append("")

    return '\n'.join(lines)


def generate_outputs_table(config: Dict[str, Any]) -> str:
    """Generate outputs by phase tables."""
    lines = []

    for i, phase in enumerate(config.get('phases', []), 1):
        orch = phase['orchestrator']
        phase_name = phase.get('name', f'Phase {i}')

        lines.append(f"### Phase {i} Outputs ({orch})")
        lines.append("")

        if phase.get('outputs'):
            lines.append("| Output | Location | Required |")
            lines.append("|--------|----------|----------|")

            for output in phase['outputs']:
                path = output['path']
                required = "Yes" if output.get('required', True) else "No"
                lines.append(f"| {path.split('/')[-1]} | `{path}` | {required} |")
        else:
            lines.append("*No outputs defined*")

        lines.append("")

    return '\n'.join(lines)


def generate_gates_section(config: Dict[str, Any]) -> str:
    """Generate gates documentation."""
    lines = []

    for i, phase in enumerate(config.get('phases', []), 1):
        if phase.get('gate'):
            gate = phase['gate']
            gate_name = gate.get('name', f'phase-{i}-gate')
            conditions = gate.get('conditions', [])

            lines.append(f"### {gate_name.replace('-', ' ').title()}")
            lines.append("")

            if conditions:
                for condition in conditions:
                    lines.append(f"- {condition}")
            else:
                lines.append("*No conditions defined*")

            lines.append("")

    return '\n'.join(lines)


def generate_chain_docs(config: Dict[str, Any]) -> str:
    """
    Generate _index.md documentation content.

    Args:
        config: Chain configuration

    Returns:
        Markdown content for _index.md
    """
    chain_name = config['name']
    description = config.get('description', f'{chain_name} skill-chain')

    content = f"""# {chain_name.replace('-', ' ').title()} - Skill-Chain Documentation

**Generated**: {datetime.now().strftime('%Y-%m-%d')}
**Version**: 1.0 (Nested Architecture)

---

## Overview

{description}

## Architecture Diagram

{generate_architecture_diagram(config)}

## Process Flow

{generate_sequence_diagram(config)}

## Skill Inventory

{generate_skill_inventory(config)}

## Outputs by Phase

{generate_outputs_table(config)}

## Gates

{generate_gates_section(config)}

## Usage Examples

```bash
# Start Phase 1
"{config['phases'][0]['orchestrator'].replace('-', ' ')}"

# Continue with Phase 2
"{config['phases'][-1]['orchestrator'].replace('-', ' ')}" if len(config.get('phases', [])) > 1 else ""
```

---

*Auto-generated documentation for {chain_name} skill-chain*
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
                'outputs': [
                    {'path': '02-resources/_briefing.md', 'required': True},
                    {'path': '02-resources/transcripts/*/_metadata.json', 'required': True},
                ],
                'gate': {
                    'name': 'readiness-gate',
                    'conditions': ['transcripts_preprocessed > 0', '_briefing.md exists'],
                },
            },
            {
                'name': 'analysis',
                'description': 'Analyze transcripts and synthesize themes',
                'orchestrator': 'execute-interview-analysis',
                'sub_skills': ['transcript-analyze', 'theme-synthesize'],
                'outputs': [
                    {'path': '02-resources/transcripts/*/index.md', 'required': True},
                    {'path': '04-outputs/_synthesis.md', 'required': True},
                ],
            },
        ],
        'shared_skills': ['transcript-analyze-core'],
    }

    print(generate_chain_docs(example_config))
