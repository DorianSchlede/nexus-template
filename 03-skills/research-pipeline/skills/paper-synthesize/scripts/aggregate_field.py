#!/usr/bin/env python3
"""
Aggregate a specific extraction field across all papers WITH sources.

This script reads the ALREADY EXTRACTED data from index.md frontmatter
and aggregates it with full source citations. No need to re-read chunks
since the extraction already includes chunk:line references.

Usage:
    python aggregate_field.py {project_path} --field ai_integration
    python aggregate_field.py {project_path} --field entity_types --output _synthesis_entities.md

Output format (markdown with sources):

    # AI Integration Patterns

    ## Pattern: Tool-Augmented LLM Reasoning
    - **Source**: 16-KG-Agent (Chunk 1:240-259)
    - **Description**: LLM uses tools to interact with KG
    - **Also found in**: 20-Agentic-RAG (Chunk 1:500-501)

    ## Pattern: Knowledge Memory State
    - **Source**: 16-KG-Agent (Chunk 1:260-275)
    ...
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any
import yaml


def parse_yaml_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith('---'):
        return {}

    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        return {}

    yaml_content = content[4:end_match.start() + 3]

    try:
        return yaml.safe_load(yaml_content) or {}
    except yaml.YAMLError:
        return {}


def normalize_pattern_name(name: str) -> str:
    """Normalize pattern name for deduplication."""
    return re.sub(r'[^a-z0-9]', '', name.lower())


def extract_field_data(papers_path: Path, field_name: str) -> dict:
    """Extract field data from all papers with sources."""

    # Structure: {normalized_name: {name, instances: [{paper_id, source, description}]}}
    patterns = defaultdict(lambda: {'name': '', 'instances': []})
    papers_with_field = []
    papers_without_field = []

    for paper_folder in sorted(papers_path.iterdir()):
        if not paper_folder.is_dir() or paper_folder.name.startswith('_'):
            continue

        index_path = paper_folder / "index.md"
        if not index_path.exists():
            continue

        paper_id = paper_folder.name

        try:
            content = index_path.read_text(encoding='utf-8')
            frontmatter = parse_yaml_frontmatter(content)
        except (IOError, UnicodeDecodeError):
            continue

        field_data = frontmatter.get(field_name)

        if not field_data:
            papers_without_field.append(paper_id)
            continue

        papers_with_field.append(paper_id)

        # Handle different field formats
        if isinstance(field_data, list):
            for item in field_data:
                if isinstance(item, dict):
                    # Structured item with name/pattern/description/source
                    name = item.get('pattern') or item.get('name') or item.get('aspect') or str(item)
                    description = item.get('description', '')
                    source = item.get('source', item.get('chunk_ref', ''))

                    normalized = normalize_pattern_name(name)
                    if not patterns[normalized]['name']:
                        patterns[normalized]['name'] = name

                    patterns[normalized]['instances'].append({
                        'paper_id': paper_id,
                        'source': source,
                        'description': description,
                        'raw': item
                    })
                elif isinstance(item, str):
                    # Simple string item
                    normalized = normalize_pattern_name(item)
                    if not patterns[normalized]['name']:
                        patterns[normalized]['name'] = item

                    patterns[normalized]['instances'].append({
                        'paper_id': paper_id,
                        'source': '',
                        'description': '',
                        'raw': item
                    })
        elif isinstance(field_data, dict):
            # Dictionary format (e.g., entity_definitions)
            for key, value in field_data.items():
                normalized = normalize_pattern_name(key)
                if not patterns[normalized]['name']:
                    patterns[normalized]['name'] = key

                description = value if isinstance(value, str) else str(value)

                patterns[normalized]['instances'].append({
                    'paper_id': paper_id,
                    'source': '',
                    'description': description,
                    'raw': {key: value}
                })
        elif isinstance(field_data, str):
            # Single string value (e.g., "N/A - paper predates...")
            if field_data.lower().startswith('n/a'):
                papers_without_field.append(paper_id)
                papers_with_field.remove(paper_id)
            else:
                patterns['_single']['name'] = field_name
                patterns['_single']['instances'].append({
                    'paper_id': paper_id,
                    'source': '',
                    'description': field_data,
                    'raw': field_data
                })

    return {
        'field': field_name,
        'patterns': dict(patterns),
        'papers_with_field': papers_with_field,
        'papers_without_field': papers_without_field,
        'total_patterns': len(patterns),
        'total_instances': sum(len(p['instances']) for p in patterns.values())
    }


def generate_markdown(data: dict, field_name: str) -> str:
    """Generate markdown synthesis with sources."""

    lines = [
        "---",
        f"field: \"{field_name}\"",
        f"synthesized_at: \"{datetime.now().isoformat()}\"",
        f"papers_included: {len(data['papers_with_field'])}",
        f"papers_excluded: {len(data['papers_without_field'])}",
        f"patterns_found: {data['total_patterns']}",
        f"total_instances: {data['total_instances']}",
        "papers_read:",
    ]
    for p in data['papers_with_field']:
        lines.append(f"  - \"{p}\"")
    lines.extend(["---", "", f"# {field_name.replace('_', ' ').title()} - Cross-Paper Synthesis", ""])

    # Summary
    lines.extend([
        "## Summary",
        "",
        f"- **Papers with data**: {len(data['papers_with_field'])}/{len(data['papers_with_field']) + len(data['papers_without_field'])}",
        f"- **Unique patterns**: {data['total_patterns']}",
        f"- **Total instances**: {data['total_instances']}",
        ""
    ])

    # Patterns sorted by frequency (most common first)
    sorted_patterns = sorted(
        data['patterns'].items(),
        key=lambda x: len(x[1]['instances']),
        reverse=True
    )

    lines.extend(["## Patterns", ""])

    for normalized, pattern_data in sorted_patterns:
        name = pattern_data['name']
        instances = pattern_data['instances']

        lines.append(f"### {name}")
        lines.append("")
        lines.append(f"**Found in {len(instances)} paper(s)**")
        lines.append("")

        for inst in instances:
            paper_id = inst['paper_id']
            source = inst['source']
            description = inst['description']

            source_str = f" (Chunk {source})" if source else ""
            lines.append(f"- **{paper_id}**{source_str}")
            if description:
                # Truncate long descriptions
                desc = description[:200] + "..." if len(description) > 200 else description
                lines.append(f"  - {desc}")

        lines.append("")

    # Papers without this field
    if data['papers_without_field']:
        lines.extend([
            "## Papers Without This Field",
            "",
            "The following papers did not have extractable data for this field:",
            ""
        ])
        for p in data['papers_without_field']:
            lines.append(f"- {p}")
        lines.append("")

    return "\n".join(lines)


def generate_yaml(data: dict) -> str:
    """Generate YAML output for programmatic use."""
    output = {
        'field': data['field'],
        'synthesized_at': datetime.now().isoformat(),
        'papers_included': data['papers_with_field'],
        'papers_excluded': data['papers_without_field'],
        'patterns': []
    }

    for normalized, pattern_data in data['patterns'].items():
        output['patterns'].append({
            'name': pattern_data['name'],
            'frequency': len(pattern_data['instances']),
            'sources': [
                {
                    'paper_id': inst['paper_id'],
                    'chunk_ref': inst['source'],
                    'description': inst['description']
                }
                for inst in pattern_data['instances']
            ]
        })

    # Sort by frequency
    output['patterns'].sort(key=lambda x: x['frequency'], reverse=True)

    return yaml.dump(output, default_flow_style=False, allow_unicode=True, sort_keys=False)


def main():
    parser = argparse.ArgumentParser(description="Aggregate extraction field across papers with sources")
    parser.add_argument("project_path", type=str, help="Path to project folder")
    parser.add_argument("--field", "-f", type=str, required=True, help="Field to aggregate")
    parser.add_argument("--output", "-o", type=str, help="Output file path")
    parser.add_argument("--format", choices=['markdown', 'yaml', 'json'], default='markdown', help="Output format")

    args = parser.parse_args()

    project_path = Path(args.project_path)
    papers_path = project_path / "02-resources" / "papers"

    if not papers_path.exists():
        print(f"Papers path not found: {papers_path}", file=sys.stderr)
        sys.exit(1)

    # Extract and aggregate
    data = extract_field_data(papers_path, args.field)

    if not data['patterns']:
        print(f"No data found for field: {args.field}", file=sys.stderr)
        sys.exit(1)

    # Generate output
    if args.format == 'markdown':
        result = generate_markdown(data, args.field)
        ext = '.md'
    elif args.format == 'yaml':
        result = generate_yaml(data)
        ext = '.yaml'
    else:
        result = json.dumps(data, indent=2, default=str)
        ext = '.json'

    # Write output
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = project_path / "04-outputs" / f"_synthesis_{args.field}{ext}"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(result, encoding='utf-8')

    # Summary
    print(f"\nField Aggregation: {args.field}")
    print("=" * 50)
    print(f"Papers with data: {len(data['papers_with_field'])}")
    print(f"Unique patterns: {data['total_patterns']}")
    print(f"Total instances: {data['total_instances']}")
    print(f"\nOutput: {output_path}")


if __name__ == "__main__":
    main()
