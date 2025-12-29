#!/usr/bin/env python3
"""
generate_chain.py - Main orchestrator for skill-chain generation

Usage:
    python generate_chain.py --name "chain-name" --config '{"json": "config"}'
    python generate_chain.py --name "chain-name" --config-file config.json

This script orchestrates the generation of a complete nested skill-chain structure.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List

# Add scripts directory to path for imports
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from generate_contract import generate_contract
from generate_parent_skill import generate_parent_skill
from generate_orchestrator import generate_orchestrator
from generate_subskill_stub import generate_subskill_stub
from generate_shared_methodology import generate_shared_methodology
from generate_chain_docs import generate_chain_docs


def validate_config(config: Dict[str, Any]) -> List[str]:
    """Validate the chain configuration, return list of errors."""
    errors = []

    # Required top-level fields
    if not config.get('name'):
        errors.append("Missing required field: 'name'")
    if not config.get('description'):
        errors.append("Missing required field: 'description'")
    if not config.get('phases'):
        errors.append("Missing required field: 'phases'")

    # Validate phases
    phases = config.get('phases', [])
    if not isinstance(phases, list):
        errors.append("'phases' must be a list")
    else:
        for i, phase in enumerate(phases):
            if not phase.get('name'):
                errors.append(f"Phase {i+1}: missing 'name'")
            if not phase.get('orchestrator'):
                errors.append(f"Phase {i+1}: missing 'orchestrator'")
            if not phase.get('sub_skills'):
                errors.append(f"Phase {i+1}: missing 'sub_skills'")

    return errors


def create_folder_structure(base_path: Path, config: Dict[str, Any]) -> Dict[str, Path]:
    """Create the nested folder structure for the skill-chain."""
    paths = {
        'root': base_path,
        'orchestrators': base_path / 'orchestrators',
        'skills': base_path / 'skills',
        'shared': base_path / 'shared',
        'validation': base_path / 'validation',
    }

    # Create main folders
    for folder in paths.values():
        folder.mkdir(parents=True, exist_ok=True)

    # Create orchestrator folders
    paths['orchestrator_skills'] = {}
    for phase in config.get('phases', []):
        orch_name = phase['orchestrator']
        orch_path = paths['orchestrators'] / orch_name
        orch_path.mkdir(exist_ok=True)
        paths['orchestrator_skills'][orch_name] = orch_path

    # Create sub-skill folders
    paths['sub_skills'] = {}
    for phase in config.get('phases', []):
        for skill_name in phase.get('sub_skills', []):
            skill_path = paths['skills'] / skill_name
            skill_path.mkdir(exist_ok=True)
            paths['sub_skills'][skill_name] = skill_path

    # Create shared methodology folders
    paths['shared_skills'] = {}
    for shared_name in config.get('shared_skills', []):
        shared_path = paths['shared'] / shared_name
        shared_path.mkdir(exist_ok=True)
        paths['shared_skills'][shared_name] = shared_path

    return paths


def generate_all(config: Dict[str, Any], output_dir: Path = None) -> Dict[str, Any]:
    """
    Generate all files for the skill-chain.

    Args:
        config: Chain configuration dictionary
        output_dir: Override output directory (default: 03-skills/{chain_name})

    Returns:
        Dictionary with generation results
    """
    chain_name = config['name']

    # Determine output directory
    if output_dir is None:
        # Find the 03-skills directory relative to this script
        skills_dir = SCRIPT_DIR.parent.parent
        output_dir = skills_dir / chain_name

    results = {
        'chain_name': chain_name,
        'output_dir': str(output_dir),
        'files_created': [],
        'errors': [],
    }

    # Validate configuration
    validation_errors = validate_config(config)
    if validation_errors:
        results['errors'] = validation_errors
        return results

    try:
        # Create folder structure
        paths = create_folder_structure(output_dir, config)
        results['folders_created'] = [str(p) for p in paths.values() if isinstance(p, Path)]

        # Generate parent SKILL.md (router)
        parent_skill_path = output_dir / 'SKILL.md'
        parent_content = generate_parent_skill(config)
        parent_skill_path.write_text(parent_content, encoding='utf-8')
        results['files_created'].append(str(parent_skill_path))

        # Generate _chain.yaml (contract)
        contract_path = output_dir / '_chain.yaml'
        contract_content = generate_contract(config)
        contract_path.write_text(contract_content, encoding='utf-8')
        results['files_created'].append(str(contract_path))

        # Generate orchestrator SKILL.md files
        for phase in config.get('phases', []):
            orch_name = phase['orchestrator']
            orch_path = paths['orchestrator_skills'][orch_name] / 'SKILL.md'
            orch_content = generate_orchestrator(config, phase)
            orch_path.write_text(orch_content, encoding='utf-8')
            results['files_created'].append(str(orch_path))

        # Generate sub-skill SKILL.md stubs
        for phase in config.get('phases', []):
            for skill_name in phase.get('sub_skills', []):
                skill_path = paths['sub_skills'][skill_name] / 'SKILL.md'
                skill_content = generate_subskill_stub(config, skill_name, phase)
                skill_path.write_text(skill_content, encoding='utf-8')
                results['files_created'].append(str(skill_path))

        # Generate shared methodology SKILL.md files
        for shared_name in config.get('shared_skills', []):
            shared_path = paths['shared_skills'][shared_name] / 'SKILL.md'
            shared_content = generate_shared_methodology(config, shared_name)
            shared_path.write_text(shared_content, encoding='utf-8')
            results['files_created'].append(str(shared_path))

        # Generate _index.md (documentation with Mermaid diagrams)
        docs_path = output_dir / '_index.md'
        docs_content = generate_chain_docs(config)
        docs_path.write_text(docs_content, encoding='utf-8')
        results['files_created'].append(str(docs_path))

        results['success'] = True

    except Exception as e:
        results['errors'].append(str(e))
        results['success'] = False

    return results


def print_results(results: Dict[str, Any]) -> None:
    """Print generation results in a formatted way."""
    chain_name = results.get('chain_name', 'unknown')

    if results.get('errors'):
        print(f"\n❌ Generation FAILED for {chain_name}")
        print("━" * 50)
        for error in results['errors']:
            print(f"  • {error}")
        return

    print(f"\n✓ Skill-chain generated: {chain_name}")
    print("━" * 50)
    print(f"\nCreated: {results['output_dir']}/")

    # Group files by type
    files = results.get('files_created', [])

    # Count by category
    orchestrators = [f for f in files if '/orchestrators/' in f.replace('\\', '/')]
    skills = [f for f in files if '/skills/' in f.replace('\\', '/')]
    shared = [f for f in files if '/shared/' in f.replace('\\', '/')]
    root_files = [f for f in files if f.replace('\\', '/').count('/') == files[0].replace('\\', '/').count('/')]

    print(f"├── SKILL.md                 ✓")
    print(f"├── _chain.yaml              ✓")
    print(f"├── _index.md                ✓")
    print(f"├── orchestrators/")
    print(f"│   └── {len(orchestrators)} orchestrator(s)  ✓")
    print(f"├── skills/")
    print(f"│   └── {len(skills)} sub-skill(s)     ✓")
    print(f"├── shared/")
    print(f"│   └── {len(shared)} shared skill(s)  ✓")
    print(f"└── validation/              ✓")

    print(f"\nTotal files created: {len(files)}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate a nested skill-chain structure'
    )
    parser.add_argument(
        '--name', '-n',
        required=True,
        help='Name of the skill-chain (kebab-case)'
    )
    parser.add_argument(
        '--config', '-c',
        help='JSON configuration string'
    )
    parser.add_argument(
        '--config-file', '-f',
        help='Path to JSON configuration file'
    )
    parser.add_argument(
        '--output-dir', '-o',
        help='Override output directory'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Validate config without creating files'
    )

    args = parser.parse_args()

    # Load configuration
    config = None
    if args.config:
        config = json.loads(args.config)
    elif args.config_file:
        with open(args.config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        print("Error: Must provide --config or --config-file")
        sys.exit(1)

    # Ensure name is set
    config['name'] = args.name

    # Validate only if dry run
    if args.dry_run:
        errors = validate_config(config)
        if errors:
            print("Validation errors:")
            for error in errors:
                print(f"  • {error}")
            sys.exit(1)
        else:
            print("✓ Configuration is valid")
            print(json.dumps(config, indent=2))
            sys.exit(0)

    # Generate
    output_dir = Path(args.output_dir) if args.output_dir else None
    results = generate_all(config, output_dir)

    print_results(results)

    sys.exit(0 if results.get('success') else 1)


if __name__ == '__main__':
    main()
