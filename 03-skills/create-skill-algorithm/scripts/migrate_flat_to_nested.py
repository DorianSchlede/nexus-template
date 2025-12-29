#!/usr/bin/env python3
"""
migrate_flat_to_nested.py - Migrate flat skill structure to nested skill-chain

Usage:
    python migrate_flat_to_nested.py --chain-name "research-pipeline" --skills-dir "03-skills"

This script helps migrate existing flat skills to a nested skill-chain structure.
It uses git mv to preserve history and updates internal references.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any


def run_git_mv(source: Path, dest: Path, dry_run: bool = False) -> bool:
    """Run git mv to move a file/folder preserving history."""
    if dry_run:
        print(f"  [DRY RUN] git mv {source} → {dest}")
        return True

    try:
        # Ensure parent directory exists
        dest.parent.mkdir(parents=True, exist_ok=True)

        result = subprocess.run(
            ['git', 'mv', str(source), str(dest)],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"  ✓ Moved: {source.name} → {dest}")
            return True
        else:
            print(f"  ✗ Failed: {source.name} - {result.stderr}")
            return False

    except Exception as e:
        print(f"  ✗ Error: {source.name} - {e}")
        return False


def categorize_skills(skills: List[str], orchestrators: List[str], shared: List[str]) -> Dict[str, str]:
    """Categorize skills into orchestrators, sub-skills, or shared."""
    categories = {}

    for skill in skills:
        if skill in orchestrators:
            categories[skill] = 'orchestrators'
        elif skill in shared:
            categories[skill] = 'shared'
        else:
            categories[skill] = 'skills'

    return categories


def update_skill_references(skill_path: Path, old_base: str, new_base: str, dry_run: bool = False):
    """Update path references in a SKILL.md file."""
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return

    content = skill_md.read_text(encoding='utf-8')
    original = content

    # Update references like "03-skills/paper-search" to relative paths
    # This is a simple pattern match - may need refinement for specific cases

    # Pattern: references to sibling skills in flat structure
    pattern = rf'{re.escape(old_base)}/([a-z-]+)/'
    replacement = lambda m: f'../../skills/{m.group(1)}/'

    content = re.sub(pattern, replacement, content)

    if content != original:
        if dry_run:
            print(f"    [DRY RUN] Would update references in {skill_md}")
        else:
            skill_md.write_text(content, encoding='utf-8')
            print(f"    Updated references in {skill_md.name}")


def create_parent_skill(chain_path: Path, config: Dict[str, Any], dry_run: bool = False):
    """Create the parent SKILL.md router."""
    parent_skill = chain_path / 'SKILL.md'

    if parent_skill.exists():
        print(f"  ! Parent SKILL.md already exists, skipping")
        return

    chain_name = config['name']
    description = config.get('description', f'{chain_name} skill-chain')

    # Build routing table
    routing_lines = []
    for phase in config.get('phases', []):
        orch = phase['orchestrator']
        routing_lines.append(f'| "{orch.replace("-", " ")}" | `orchestrators/{orch}/SKILL.md` |')
        for skill in phase.get('sub_skills', []):
            routing_lines.append(f'| "{skill.replace("-", " ")}" | `skills/{skill}/SKILL.md` |')

    routing_table = '\n'.join(routing_lines)

    content = f"""---
name: {chain_name}
description: "{description}. This is the MASTER entry point - routes to appropriate child skills."
type: skill-chain
version: "1.0"
---

# {chain_name.replace('-', ' ').title()}

{description}

**This is a CONNECT/ROUTER skill** - routes to specialized skills.

## Routing Table

| User Intent | Route To |
|-------------|----------|
{routing_table}

## Chain Documentation

- **Contract**: See `_chain.yaml` for validation contract
- **Documentation**: See `_index.md` for auto-generated docs

---

*Migrated to nested structure*
"""

    if dry_run:
        print(f"  [DRY RUN] Would create parent SKILL.md")
    else:
        parent_skill.write_text(content, encoding='utf-8')
        print(f"  ✓ Created parent SKILL.md")


def migrate(
    skills_dir: Path,
    chain_name: str,
    skill_names: List[str],
    orchestrators: List[str],
    shared: List[str],
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Migrate flat skills to nested structure.

    Args:
        skills_dir: Path to 03-skills directory
        chain_name: Name of the new chain (e.g., "research-pipeline")
        skill_names: List of skill folder names to migrate
        orchestrators: List of skill names that are orchestrators
        shared: List of skill names that are shared methodologies
        dry_run: If True, don't make changes, just show what would happen

    Returns:
        Migration results
    """
    results = {
        'chain_name': chain_name,
        'skills_moved': [],
        'errors': [],
        'dry_run': dry_run,
    }

    chain_path = skills_dir / chain_name

    print(f"\n{'[DRY RUN] ' if dry_run else ''}Migrating to: {chain_path}")
    print("=" * 60)

    # Create chain folder structure
    if not dry_run:
        (chain_path / 'orchestrators').mkdir(parents=True, exist_ok=True)
        (chain_path / 'skills').mkdir(parents=True, exist_ok=True)
        (chain_path / 'shared').mkdir(parents=True, exist_ok=True)
        (chain_path / 'validation').mkdir(parents=True, exist_ok=True)
    print(f"✓ Created folder structure")

    # Categorize skills
    categories = categorize_skills(skill_names, orchestrators, shared)

    # Move each skill
    print(f"\nMoving {len(skill_names)} skills:")
    for skill_name in skill_names:
        source = skills_dir / skill_name
        category = categories[skill_name]
        dest = chain_path / category / skill_name

        if not source.exists():
            print(f"  ! Skipping {skill_name} (not found)")
            results['errors'].append(f"Not found: {skill_name}")
            continue

        if dest.exists():
            print(f"  ! Skipping {skill_name} (already exists at destination)")
            continue

        if run_git_mv(source, dest, dry_run):
            results['skills_moved'].append({
                'name': skill_name,
                'from': str(source),
                'to': str(dest),
                'category': category,
            })

            # Update internal references
            if not dry_run:
                update_skill_references(dest, str(skills_dir), str(chain_path), dry_run)

    # Create config for parent skill
    config = {
        'name': chain_name,
        'description': f'{chain_name.replace("-", " ").title()} skill-chain',
        'phases': [],
    }

    # Build phases from orchestrators
    for i, orch in enumerate(orchestrators, 1):
        phase = {
            'name': f'phase-{i}',
            'orchestrator': orch,
            'sub_skills': [s for s in skill_names if categories.get(s) == 'skills'],
        }
        config['phases'].append(phase)

    config['shared_skills'] = shared

    # Create parent SKILL.md
    print(f"\nCreating parent SKILL.md:")
    create_parent_skill(chain_path, config, dry_run)

    # Summary
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Migration Summary:")
    print(f"  - Skills moved: {len(results['skills_moved'])}")
    print(f"  - Errors: {len(results['errors'])}")

    if results['errors']:
        print(f"\nErrors:")
        for error in results['errors']:
            print(f"  - {error}")

    print(f"\nNext steps:")
    print(f"  1. Create _chain.yaml contract")
    print(f"  2. Generate _index.md documentation")
    print(f"  3. Update SKILL.md routing table with correct triggers")
    print(f"  4. Test that all skills work correctly")

    return results


def main():
    parser = argparse.ArgumentParser(
        description='Migrate flat skills to nested skill-chain structure'
    )
    parser.add_argument(
        '--chain-name', '-n',
        required=True,
        help='Name of the new skill-chain (kebab-case)'
    )
    parser.add_argument(
        '--skills-dir', '-d',
        default='03-skills',
        help='Path to skills directory (default: 03-skills)'
    )
    parser.add_argument(
        '--skills', '-s',
        required=True,
        help='Comma-separated list of skill names to migrate'
    )
    parser.add_argument(
        '--orchestrators', '-o',
        required=True,
        help='Comma-separated list of orchestrator skill names'
    )
    parser.add_argument(
        '--shared',
        default='',
        help='Comma-separated list of shared methodology skill names'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )

    args = parser.parse_args()

    skills_dir = Path(args.skills_dir)
    skill_names = [s.strip() for s in args.skills.split(',')]
    orchestrators = [s.strip() for s in args.orchestrators.split(',')]
    shared = [s.strip() for s in args.shared.split(',')] if args.shared else []

    results = migrate(
        skills_dir=skills_dir,
        chain_name=args.chain_name,
        skill_names=skill_names,
        orchestrators=orchestrators,
        shared=shared,
        dry_run=args.dry_run,
    )

    sys.exit(0 if not results['errors'] else 1)


if __name__ == '__main__':
    main()
