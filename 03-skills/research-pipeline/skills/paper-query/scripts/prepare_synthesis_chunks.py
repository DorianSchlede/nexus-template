#!/usr/bin/env python3
"""
Prepare chunk routing for synthesis by mapping research questions to relevant chunks.

This script analyzes all index.md files and creates a routing table that tells
subagents exactly which chunks to read for each synthesis question/field.

Workflow:
1. Read _briefing.md to get research question and extraction fields
2. Read all index.md files to get:
   - YAML frontmatter (extracted data)
   - Chunk navigation with "Load when" hints
3. Match extraction fields to "Load when" hints
4. Output a routing table: {field -> [(paper, chunks_to_read)]}

Usage:
    python prepare_synthesis_chunks.py 02-projects/02-ontologies-research

Output:
    02-resources/_synthesis_routing.yaml

Example output:
    ai_integration:
      - paper_id: 16-KG-Agent
        chunks: [1, 2]
        reason: "Load when mentions 'agent reasoning', 'tool use'"
      - paper_id: 20-Agentic_RAG
        chunks: [1, 3]
        reason: "Load when mentions 'agentic patterns'"
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

    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        return {}

    yaml_content = content[4:end_match.start() + 3]

    try:
        return yaml.safe_load(yaml_content) or {}
    except yaml.YAMLError:
        return {}


def extract_chunk_navigation(content: str) -> list[dict]:
    """Extract chunk navigation with 'Load when' hints from index.md."""
    chunks = []

    # Find "## Chunk Navigation" section
    nav_match = re.search(r'## Chunk Navigation\s*\n', content)
    if not nav_match:
        return chunks

    nav_section = content[nav_match.end():]

    # Find each chunk header
    chunk_pattern = r'### Chunk (\d+):\s*([^\n]+)\n(.*?)(?=### Chunk|\Z)'
    for match in re.finditer(chunk_pattern, nav_section, re.DOTALL):
        chunk_num = int(match.group(1))
        chunk_title = match.group(2).strip()
        chunk_content = match.group(3)

        # Extract "Load when" hint
        load_when_match = re.search(r'\*\*Load when\*\*:\s*([^\n]+)', chunk_content)
        load_when = load_when_match.group(1).strip() if load_when_match else ""

        # Extract key concepts
        concepts_match = re.search(r'\*\*Key concepts\*\*:\s*\[([^\]]+)\]', chunk_content)
        concepts = concepts_match.group(1).split(',') if concepts_match else []
        concepts = [c.strip().strip('"\'') for c in concepts]

        chunks.append({
            'chunk_num': chunk_num,
            'title': chunk_title,
            'load_when': load_when,
            'concepts': concepts
        })

    return chunks


def match_field_to_chunks(field_name: str, field_def: str, paper_chunks: list[dict]) -> list[int]:
    """Find chunks relevant to a field based on 'Load when' hints and concepts."""
    relevant_chunks = []

    # Keywords to look for based on field name
    field_keywords = {
        'entity_types': ['entity', 'type', 'class', 'ontology', 'concept', 'definition'],
        'entity_definitions': ['entity', 'definition', 'concept', 'ontology'],
        'entity_relationships': ['relationship', 'relation', 'connection', 'link'],
        'framework_comparison': ['framework', 'comparison', 'compare', 'versus', 'vs'],
        'ai_integration': ['AI', 'LLM', 'agent', 'integration', 'neural', 'learning'],
        'agent_modeling': ['agent', 'model', 'behavior', 'capability', 'architecture'],
        'agentic_workflows': ['workflow', 'pattern', 'process', 'orchestration', 'pipeline'],
        'generative_ai_patterns': ['generative', 'LLM', 'prompt', 'generation', 'pattern'],
        'agent_ontology_integration': ['agent', 'ontology', 'integration', 'knowledge'],
        'methodology': ['method', 'approach', 'methodology', 'technique'],
        'empirical_evidence': ['evidence', 'evaluation', 'experiment', 'benchmark', 'result'],
        'limitations': ['limitation', 'constraint', 'weakness', 'future'],
    }

    keywords = field_keywords.get(field_name, [field_name.replace('_', ' ')])

    for chunk in paper_chunks:
        # Check load_when hint
        load_when_lower = chunk['load_when'].lower()
        concepts_lower = ' '.join(chunk['concepts']).lower()
        title_lower = chunk['title'].lower()

        # Score based on keyword matches
        score = 0
        for kw in keywords:
            kw_lower = kw.lower()
            if kw_lower in load_when_lower:
                score += 3  # High weight for load_when match
            if kw_lower in concepts_lower:
                score += 2  # Medium weight for concept match
            if kw_lower in title_lower:
                score += 1  # Low weight for title match

        if score > 0:
            relevant_chunks.append((chunk['chunk_num'], score))

    # Sort by score descending, return chunk numbers
    relevant_chunks.sort(key=lambda x: -x[1])
    return [c[0] for c in relevant_chunks]


def prepare_routing(project_path: Path) -> dict:
    """Prepare synthesis routing table for all fields."""
    papers_path = project_path / "02-resources" / "papers"
    briefing_path = project_path / "02-resources" / "_briefing.md"

    if not papers_path.exists():
        raise FileNotFoundError(f"Papers path not found: {papers_path}")

    # Read briefing to get extraction fields
    extraction_fields = []
    if briefing_path.exists():
        briefing_content = briefing_path.read_text(encoding='utf-8')
        briefing_fm = parse_yaml_frontmatter(briefing_content)
        extraction_schema = briefing_fm.get('extraction_schema', [])
        for field in extraction_schema:
            if isinstance(field, dict):
                extraction_fields.append({
                    'name': field.get('field', ''),
                    'description': field.get('description', ''),
                    'priority': field.get('priority', 'medium')
                })

    # If no briefing, infer fields from first paper's frontmatter
    if not extraction_fields:
        for paper_folder in papers_path.iterdir():
            if paper_folder.is_dir() and not paper_folder.name.startswith('_'):
                index_path = paper_folder / "index.md"
                if index_path.exists():
                    content = index_path.read_text(encoding='utf-8')
                    fm = parse_yaml_frontmatter(content)
                    # Use high-priority fields from first paper
                    for key in ['entity_types', 'framework_comparison', 'ai_integration',
                               'agent_modeling', 'agentic_workflows', 'generative_ai_patterns',
                               'agent_ontology_integration']:
                        if key in fm:
                            extraction_fields.append({
                                'name': key,
                                'description': f'Extracted {key}',
                                'priority': 'high'
                            })
                    break

    # Build routing table
    routing = {
        'project': str(project_path),
        'fields': {},
        'papers_analyzed': 0
    }

    for paper_folder in sorted(papers_path.iterdir()):
        if not paper_folder.is_dir() or paper_folder.name.startswith('_'):
            continue

        index_path = paper_folder / "index.md"
        if not index_path.exists():
            continue

        routing['papers_analyzed'] += 1

        content = index_path.read_text(encoding='utf-8')
        frontmatter = parse_yaml_frontmatter(content)
        chunks = extract_chunk_navigation(content)

        paper_id = paper_folder.name

        # For each extraction field, find relevant chunks
        for field in extraction_fields:
            field_name = field['name']

            # Check if paper has this field
            if field_name not in frontmatter or not frontmatter[field_name]:
                continue

            # Initialize field in routing if needed
            if field_name not in routing['fields']:
                routing['fields'][field_name] = {
                    'description': field['description'],
                    'priority': field['priority'],
                    'papers': []
                }

            # Find relevant chunks
            relevant_chunks = match_field_to_chunks(field_name, field['description'], chunks)

            # If no specific chunks matched, default to chunk 1 (usually intro/overview)
            if not relevant_chunks and chunks:
                relevant_chunks = [1]

            # Get item count from frontmatter
            field_data = frontmatter[field_name]
            item_count = len(field_data) if isinstance(field_data, list) else 1

            routing['fields'][field_name]['papers'].append({
                'paper_id': paper_id,
                'chunks_to_read': relevant_chunks[:3],  # Top 3 most relevant
                'items_extracted': item_count,
                'has_data': True
            })

    return routing


def main():
    parser = argparse.ArgumentParser(description="Prepare chunk routing for synthesis")
    parser.add_argument("project_path", type=str, help="Path to project folder")
    parser.add_argument("--output", "-o", type=str, help="Output file (default: 02-resources/_synthesis_routing.yaml)")
    parser.add_argument("--format", "-f", choices=['yaml', 'json'], default='yaml', help="Output format")

    args = parser.parse_args()

    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"Project path not found: {project_path}", file=sys.stderr)
        sys.exit(1)

    try:
        routing = prepare_routing(project_path)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Output
    output_path = args.output or str(project_path / "02-resources" / "_synthesis_routing.yaml")

    if args.format == 'json':
        result = json.dumps(routing, indent=2)
        if not output_path.endswith('.json'):
            output_path = output_path.replace('.yaml', '.json')
    else:
        result = yaml.dump(routing, default_flow_style=False, allow_unicode=True, sort_keys=False)

    Path(output_path).write_text(result, encoding='utf-8')

    # Summary
    print(f"\nSynthesis Routing Prepared")
    print("=" * 50)
    print(f"Papers analyzed: {routing['papers_analyzed']}")
    print(f"Fields mapped: {len(routing['fields'])}")
    print()

    for field_name, field_data in routing['fields'].items():
        paper_count = len(field_data['papers'])
        total_chunks = sum(len(p['chunks_to_read']) for p in field_data['papers'])
        print(f"  {field_name}: {paper_count} papers, {total_chunks} chunks to read")

    print(f"\nRouting saved to: {output_path}")


if __name__ == "__main__":
    main()
