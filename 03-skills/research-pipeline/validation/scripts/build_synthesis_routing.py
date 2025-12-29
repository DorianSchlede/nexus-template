#!/usr/bin/env python3
"""
build_synthesis_routing.py - Level 1 of 7-Level Synthesis Architecture

Builds synthesis routing table from chunk_index.fields_found in index.md files.
Uses boolean lookup (no full-text search) for deterministic routing.

Gap G19 Fix: Warns if field matches >80% of chunks (sparsity check).

Usage:
    python build_synthesis_routing.py PROJECT_PATH --output ROUTING_FILE
    python build_synthesis_routing.py 02-projects/02-ontologies-research --output 02-resources/_synthesis_routing.yaml
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import yaml
import re


def parse_yaml_frontmatter(content: str) -> Dict[str, Any]:
    """Parse YAML frontmatter from markdown file."""
    if not content.startswith('---'):
        return {}

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}

    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return {}


def read_briefing(project_path: Path) -> Dict[str, Any]:
    """Read _briefing.md to get extraction schema."""
    briefing_path = project_path / "02-resources" / "_briefing.md"
    if not briefing_path.exists():
        print(f"ERROR: Missing _briefing.md at {briefing_path}", file=sys.stderr)
        sys.exit(1)

    content = briefing_path.read_text(encoding='utf-8')
    frontmatter = parse_yaml_frontmatter(content)

    # Support both extraction_schema and extraction_fields (different briefing formats)
    if 'extraction_schema' not in frontmatter and 'extraction_fields' not in frontmatter:
        print(f"ERROR: _briefing.md missing extraction_schema or extraction_fields", file=sys.stderr)
        sys.exit(1)

    # Normalize to extraction_schema format
    if 'extraction_fields' in frontmatter and 'extraction_schema' not in frontmatter:
        # Convert extraction_fields (with 'name') to extraction_schema (with 'field')
        frontmatter['extraction_schema'] = [
            {
                'field': f['name'],
                'description': f.get('description', ''),
                'priority': 'high' if 'pattern' in f['name'] or 'mechanism' in f['name'] else 'medium'
            }
            for f in frontmatter['extraction_fields']
        ]

    return frontmatter


def read_index_files(project_path: Path) -> List[Dict[str, Any]]:
    """Read all index.md files with chunk_index."""
    papers_path = project_path / "02-resources" / "papers"
    if not papers_path.exists():
        print(f"ERROR: Papers directory not found at {papers_path}", file=sys.stderr)
        sys.exit(1)

    indices = []
    for paper_dir in papers_path.iterdir():
        if not paper_dir.is_dir():
            continue

        index_path = paper_dir / "index.md"
        if not index_path.exists():
            continue

        content = index_path.read_text(encoding='utf-8')
        frontmatter = parse_yaml_frontmatter(content)

        # Check for chunk_index (Schema 2.3+)
        if 'chunk_index' not in frontmatter:
            print(f"WARNING: {paper_dir.name}/index.md missing chunk_index (legacy schema)", file=sys.stderr)
            continue

        indices.append({
            'paper_id': paper_dir.name,
            'paper_path': str(paper_dir),
            'chunk_index': frontmatter['chunk_index'],
            'frontmatter': frontmatter
        })

    return indices


def build_routing(indices: List[Dict], briefing: Dict) -> Dict[str, Any]:
    """Build routing table from chunk_index.fields_found."""
    extraction_schema = briefing['extraction_schema']
    field_names = [f['field'] for f in extraction_schema]

    # Initialize routing structure
    routing = {
        'project': '',
        'generated_at': datetime.now().isoformat(),
        'algorithm': 'boolean_lookup',
        'fields': {},
        'stats': {
            'papers_analyzed': len(indices),
            'total_chunks': 0,
            'chunks_per_field_avg': 0
        }
    }

    # Build field routing
    for field_spec in extraction_schema:
        field_name = field_spec['field']
        priority = field_spec.get('priority', 'medium')
        description = field_spec.get('description', '')

        field_data = {
            'description': description,
            'priority': priority,
            'sparsity_warning': False,
            'chunks': []
        }

        # Scan all chunks for this field
        for paper in indices:
            paper_id = paper['paper_id']
            chunk_index = paper['chunk_index']

            for chunk_num_str, chunk_data in chunk_index.items():
                chunk_num = int(chunk_num_str) if isinstance(chunk_num_str, str) else chunk_num_str
                fields_found = chunk_data.get('fields_found', {})

                # Check if field is true or partial
                field_state = fields_found.get(field_name, False)
                if field_state in [True, 'true', 'partial']:
                    field_data['chunks'].append({
                        'paper_id': paper_id,
                        'chunk': chunk_num,
                        'fields_found_state': field_state if isinstance(field_state, str) else ('true' if field_state else 'false'),
                        'token_count': chunk_data.get('token_count', 0)
                    })

        routing['fields'][field_name] = field_data

    # Calculate stats
    total_chunks = sum(
        len(paper['chunk_index'])
        for paper in indices
    )
    routing['stats']['total_chunks'] = total_chunks

    # Sparsity check (Gap G19)
    total_chunks_per_field = []
    for field_name, field_data in routing['fields'].items():
        field_chunks = len(field_data['chunks'])
        total_chunks_per_field.append(field_chunks)

        # Check if field matches >80% of chunks
        if total_chunks > 0:
            match_rate = field_chunks / total_chunks
            if match_rate > 0.8:
                field_data['sparsity_warning'] = True
                field_data['match_rate'] = f"{match_rate:.1%}"
                print(f"WARNING (Gap G19): Field '{field_name}' matches {match_rate:.1%} of chunks (>80% threshold)", file=sys.stderr)

    if total_chunks_per_field:
        routing['stats']['chunks_per_field_avg'] = sum(total_chunks_per_field) // len(total_chunks_per_field)

    return routing


def main():
    parser = argparse.ArgumentParser(
        description='Build synthesis routing table from chunk_index (Level 1 of 7-Level Architecture)'
    )
    parser.add_argument('project_path', type=Path, help='Path to research project')
    parser.add_argument('--output', '-o', type=Path, required=True, help='Output routing YAML file')
    args = parser.parse_args()

    project_path = args.project_path
    if not project_path.is_absolute():
        project_path = Path.cwd() / project_path

    if not project_path.exists():
        print(f"ERROR: Project path not found: {project_path}", file=sys.stderr)
        sys.exit(1)

    # Read inputs
    print(f"Reading briefing from {project_path}...")
    briefing = read_briefing(project_path)

    print("Scanning index.md files for chunk_index...")
    indices = read_index_files(project_path)

    if not indices:
        print("ERROR: No index.md files with chunk_index found", file=sys.stderr)
        print("Re-analyze papers with Schema 2.3+ to add chunk_index", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(indices)} papers with chunk_index")

    # Build routing
    print("Building routing table...")
    routing = build_routing(indices, briefing)
    routing['project'] = str(project_path)

    # Write output
    output_path = args.output
    if not output_path.is_absolute():
        output_path = project_path / output_path

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(routing, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"\nLevel 1 Complete: Routing table written to {output_path}")
    print(f"  Fields: {len(routing['fields'])}")
    print(f"  Total chunks routed: {routing['stats']['total_chunks']}")

    # Report sparsity warnings
    sparse_fields = [f for f, d in routing['fields'].items() if d.get('sparsity_warning')]
    if sparse_fields:
        print(f"\n⚠️  SPARSITY WARNINGS (Gap G19):")
        for f in sparse_fields:
            print(f"   - {f}: {routing['fields'][f].get('match_rate', '>80%')}")


if __name__ == '__main__':
    main()
