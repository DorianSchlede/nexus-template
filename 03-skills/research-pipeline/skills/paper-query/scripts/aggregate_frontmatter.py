#!/usr/bin/env python3
"""
Aggregate all YAML frontmatter from index.md files into a single queryable file.

This enables efficient synthesis by:
1. Collecting all extracted data in one place
2. Identifying which papers have data for specific fields
3. Supporting cross-paper pattern detection

Usage:
    # Aggregate all frontmatter to YAML
    python aggregate_frontmatter.py 02-projects/02-ontologies-research/02-resources/papers

    # Query which papers have a specific field
    python aggregate_frontmatter.py 02-projects/.../papers --query ai_integration

    # Output to specific file
    python aggregate_frontmatter.py 02-projects/.../papers --output _aggregated.yaml
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any
import yaml


def parse_yaml_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith('---'):
        return {}

    # Find end of frontmatter
    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        return {}

    yaml_content = content[4:end_match.start() + 3]

    try:
        return yaml.safe_load(yaml_content) or {}
    except yaml.YAMLError:
        # Fallback to simple parsing for malformed YAML
        return parse_yaml_simple(yaml_content)


def parse_yaml_simple(yaml_content: str) -> dict:
    """Simple YAML parser for basic key-value pairs."""
    result = {}
    current_key = None
    current_list = None

    for line in yaml_content.split('\n'):
        line = line.rstrip()
        if not line or line.startswith('#'):
            continue

        # List item
        if line.startswith('  - ') and current_key:
            if current_list is None:
                current_list = []
            current_list.append(line[4:].strip().strip('"\''))
            result[current_key] = current_list
            continue

        # Key-value pair
        if ':' in line and not line.startswith(' '):
            if current_list is not None:
                current_list = None

            key, _, value = line.partition(':')
            key = key.strip()
            value = value.strip()
            current_key = key

            if value:
                if value.isdigit():
                    result[key] = int(value)
                elif value.lower() in ('true', 'false'):
                    result[key] = value.lower() == 'true'
                elif value.startswith('"') and value.endswith('"'):
                    result[key] = value[1:-1]
                else:
                    result[key] = value

    return result


def get_field_summary(papers: dict, field: str) -> dict:
    """Get summary of which papers have data for a specific field."""
    summary = {
        'field': field,
        'papers_with_field': [],
        'papers_without_field': [],
        'total_items': 0,
        'sample_values': []
    }

    for paper_id, frontmatter in papers.items():
        value = frontmatter.get(field)
        if value:
            summary['papers_with_field'].append(paper_id)
            if isinstance(value, list):
                summary['total_items'] += len(value)
                if len(summary['sample_values']) < 5 and value:
                    summary['sample_values'].extend(value[:2])
            elif isinstance(value, dict):
                summary['total_items'] += len(value)
        else:
            summary['papers_without_field'].append(paper_id)

    return summary


def aggregate_papers(papers_root: Path) -> dict:
    """Aggregate frontmatter from all index.md files."""
    papers = {}

    for paper_folder in sorted(papers_root.iterdir()):
        if not paper_folder.is_dir() or paper_folder.name.startswith('_'):
            continue

        index_path = paper_folder / "index.md"
        if not index_path.exists():
            continue

        try:
            content = index_path.read_text(encoding='utf-8')
            frontmatter = parse_yaml_frontmatter(content)

            if frontmatter:
                papers[paper_folder.name] = frontmatter
        except (IOError, UnicodeDecodeError) as e:
            print(f"Warning: Could not read {index_path}: {e}", file=sys.stderr)

    return papers


def main():
    parser = argparse.ArgumentParser(description="Aggregate frontmatter from paper index.md files")
    parser.add_argument("papers_root", type=str, help="Path to papers folder")
    parser.add_argument("--output", "-o", type=str, help="Output file path (default: stdout)")
    parser.add_argument("--query", "-q", type=str, help="Query which papers have a specific field")
    parser.add_argument("--format", "-f", choices=['yaml', 'json'], default='yaml', help="Output format")
    parser.add_argument("--fields", type=str, help="Comma-separated list of fields to include (default: all)")
    parser.add_argument("--summary", "-s", action="store_true", help="Output field summary instead of full data")

    args = parser.parse_args()

    papers_root = Path(args.papers_root)
    if not papers_root.exists():
        print(f"Papers root not found: {papers_root}", file=sys.stderr)
        sys.exit(1)

    # Aggregate all papers
    papers = aggregate_papers(papers_root)

    if not papers:
        print("No papers with index.md found", file=sys.stderr)
        sys.exit(1)

    # Filter fields if specified
    if args.fields:
        field_list = [f.strip() for f in args.fields.split(',')]
        papers = {
            paper_id: {k: v for k, v in fm.items() if k in field_list}
            for paper_id, fm in papers.items()
        }

    # Query mode
    if args.query:
        summary = get_field_summary(papers, args.query)

        print(f"\nField Query: {args.query}")
        print("=" * 50)
        print(f"Papers with field: {len(summary['papers_with_field'])}")
        print(f"Papers without field: {len(summary['papers_without_field'])}")
        print(f"Total items extracted: {summary['total_items']}")

        if summary['papers_with_field']:
            print(f"\nPapers with '{args.query}':")
            for p in summary['papers_with_field'][:10]:
                print(f"  - {p}")
            if len(summary['papers_with_field']) > 10:
                print(f"  ... and {len(summary['papers_with_field']) - 10} more")

        if summary['sample_values']:
            print(f"\nSample values:")
            for v in summary['sample_values'][:5]:
                if isinstance(v, dict):
                    print(f"  - {v.get('pattern', v.get('name', str(v)[:50]))}")
                else:
                    print(f"  - {str(v)[:60]}")

        return

    # Summary mode
    if args.summary:
        all_fields = set()
        for fm in papers.values():
            all_fields.update(fm.keys())

        print(f"\nPapers Aggregated: {len(papers)}")
        print("=" * 50)
        print("\nFields found across papers:")

        for field in sorted(all_fields):
            count = sum(1 for fm in papers.values() if fm.get(field))
            pct = count / len(papers) * 100
            print(f"  {field}: {count}/{len(papers)} papers ({pct:.0f}%)")

        return

    # Full output
    output = {
        'aggregated_at': str(Path(args.papers_root).resolve()),
        'paper_count': len(papers),
        'papers': papers
    }

    if args.format == 'json':
        result = json.dumps(output, indent=2, default=str)
    else:
        result = yaml.dump(output, default_flow_style=False, allow_unicode=True, sort_keys=False)

    if args.output:
        Path(args.output).write_text(result, encoding='utf-8')
        print(f"Aggregated {len(papers)} papers to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
