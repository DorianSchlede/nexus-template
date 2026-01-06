#!/usr/bin/env python3
"""
generate_contract.py - Generate _chain.yaml contract for skill-chains

The contract defines:
- Chain structure and metadata
- All skills with their paths
- Outputs per skill (required/optional)
- Gate conditions between phases
- Schema definitions for validation
"""

from typing import Dict, Any, List
from datetime import datetime
import yaml


def generate_contract(config: Dict[str, Any]) -> str:
    """
    Generate _chain.yaml contract content.

    Args:
        config: Chain configuration with phases, skills, outputs, gates

    Returns:
        YAML string for _chain.yaml
    """
    chain_name = config['name']
    description = config.get('description', f'{chain_name} skill-chain')

    # Build the contract structure
    contract = {
        'name': chain_name,
        'version': '1.0',
        'description': description,
        'generated': datetime.now().strftime('%Y-%m-%d'),
        'structure': {
            'type': 'nested',
            'parent_skill': 'SKILL.md',
            'subfolders': ['orchestrators', 'skills', 'shared', 'validation'],
        },
        'skills': [],
        'schemas': {},
        'gates': {},
    }

    # Add orchestrators and sub-skills
    for i, phase in enumerate(config.get('phases', []), 1):
        # Orchestrator
        orch_name = phase['orchestrator']
        orch_skill = {
            'id': orch_name,
            'phase': i,
            'type': 'orchestrator',
            'path': f'orchestrators/{orch_name}/SKILL.md',
            'description': phase.get('description', f'Phase {i} orchestrator'),
            'uses': phase.get('sub_skills', []),
        }

        # Add outputs if defined
        if phase.get('outputs'):
            orch_skill['produces'] = []
            for output in phase['outputs']:
                output_entry = {'path': output['path']}
                if output.get('required', True):
                    output_entry['required'] = True
                if output.get('schema'):
                    output_entry['schema'] = output['schema']
                if output.get('validates'):
                    output_entry['validates'] = output['validates']
                if output.get('min_count'):
                    output_entry['min_count'] = output['min_count']
                orch_skill['produces'].append(output_entry)

        # Add gate reference
        if phase.get('gate'):
            orch_skill['gate'] = phase['gate'].get('name', f'phase-{i}-gate')

        contract['skills'].append(orch_skill)

        # Sub-skills
        for skill_name in phase.get('sub_skills', []):
            sub_skill = {
                'id': skill_name,
                'phase': i,
                'type': 'sub-skill',
                'path': f'skills/{skill_name}/SKILL.md',
                'called_by': orch_name,
            }
            contract['skills'].append(sub_skill)

    # Add shared methodologies
    for shared_name in config.get('shared_skills', []):
        shared_skill = {
            'id': shared_name,
            'type': 'shared-methodology',
            'path': f'shared/{shared_name}/SKILL.md',
            'note': 'DO NOT LOAD DIRECTLY - loaded by subagents',
        }
        contract['skills'].append(shared_skill)

    # Add gates
    for i, phase in enumerate(config.get('phases', []), 1):
        if phase.get('gate'):
            gate_name = phase['gate'].get('name', f'phase-{i}-gate')
            gate_conditions = phase['gate'].get('conditions', [])
            contract['gates'][gate_name] = {
                'after_phase': i,
                'checks': gate_conditions,
            }

    # Add schemas if defined
    for schema_name, schema_def in config.get('schemas', {}).items():
        contract['schemas'][schema_name] = schema_def

    # Convert to YAML with nice formatting
    yaml_content = yaml.dump(
        contract,
        default_flow_style=False,
        sort_keys=False,
        allow_unicode=True,
        width=100,
    )

    # Add header comment
    header = f"""# {chain_name} Skill-Chain Contract
# Generated: {datetime.now().strftime('%Y-%m-%d')}
#
# This file defines the structure, skills, outputs, and gates for the skill-chain.
# Used by validation tools to verify chain execution.

"""

    return header + yaml_content


def contract_from_minimal(name: str, description: str, phases: List[Dict]) -> str:
    """
    Generate contract from minimal configuration.

    Args:
        name: Chain name (kebab-case)
        description: Brief description
        phases: List of phase definitions

    Returns:
        YAML contract string
    """
    config = {
        'name': name,
        'description': description,
        'phases': phases,
    }
    return generate_contract(config)


if __name__ == '__main__':
    # Example usage
    example_config = {
        'name': 'interview-analysis',
        'description': 'Analyze interview transcripts for themes and insights',
        'phases': [
            {
                'name': 'preparation',
                'orchestrator': 'prepare-interview-project',
                'sub_skills': ['transcript-import', 'transcript-preprocess'],
                'outputs': [
                    {'path': '02-resources/_briefing.md', 'required': True},
                    {'path': '02-resources/transcripts/*/_metadata.json', 'required': True, 'min_count': 1},
                ],
                'gate': {
                    'name': 'readiness-gate',
                    'conditions': ['transcripts_preprocessed > 0', '_briefing.md exists'],
                },
            },
            {
                'name': 'analysis',
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

    print(generate_contract(example_config))
