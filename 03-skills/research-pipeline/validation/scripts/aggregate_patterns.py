#!/usr/bin/env python3
"""
aggregate_patterns.py - Level 6 of 7-Level Synthesis Architecture

Aggregates patterns from batch extractions into per-field synthesis files.
Uses fuzzy matching to deduplicate patterns while preserving all sources.

Usage:
    python aggregate_patterns.py PROJECT_PATH --input-dir WORKING_DIR --output-dir OUTPUTS_DIR
"""

import argparse
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple
from collections import defaultdict
import yaml


def load_yaml(path: Path) -> Dict[str, Any]:
    """Load YAML file, handling multi-document YAML (frontmatter + body)."""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Handle multi-document YAML (frontmatter + body pattern)
    # Merge all documents into a single dict
    result = {}
    for doc in yaml.safe_load_all(content):
        if doc:
            result.update(doc)
    return result


def normalize_name(name: str) -> str:
    """Normalize pattern name for comparison."""
    # Lowercase, remove punctuation, collapse whitespace
    normalized = name.lower()
    normalized = re.sub(r'[^\w\s]', '', normalized)
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    return normalized


def similarity_ratio(a: str, b: str) -> float:
    """
    Calculate simple similarity ratio between two strings.

    Uses character-level comparison for efficiency.
    """
    a_norm = normalize_name(a)
    b_norm = normalize_name(b)

    if not a_norm or not b_norm:
        return 0.0

    # Use length-weighted character matching
    longer = max(len(a_norm), len(b_norm))
    matches = sum(1 for i, c in enumerate(a_norm) if i < len(b_norm) and c == b_norm[i])

    return matches / longer


def find_matching_pattern(
    pattern_name: str,
    existing_patterns: Dict[str, Dict],
    threshold: float = 0.7
) -> Tuple[str, float]:
    """
    Find existing pattern that matches the given name.

    Returns: (matching_key, similarity_score) or (None, 0.0) if no match
    """
    best_match = None
    best_score = 0.0

    pattern_normalized = normalize_name(pattern_name)

    for existing_key, existing_data in existing_patterns.items():
        existing_normalized = normalize_name(existing_key)

        # Check exact match first
        if pattern_normalized == existing_normalized:
            return (existing_key, 1.0)

        # Check similarity
        score = similarity_ratio(pattern_name, existing_key)
        if score > best_score and score >= threshold:
            best_match = existing_key
            best_score = score

    return (best_match, best_score) if best_match else (None, 0.0)


def aggregate_field(batch_files: List[Path], field_name: str) -> Dict[str, Any]:
    """
    Aggregate patterns for a single field from multiple batch files.

    Returns aggregated field data with deduplicated patterns.
    """
    # Track patterns by normalized name
    patterns: Dict[str, Dict] = {}

    total_patterns_in = 0
    batches_merged = 0

    for batch_path in batch_files:
        batch_data = load_yaml(batch_path)

        if batch_data.get('field') != field_name:
            continue

        batches_merged += 1
        batch_patterns = batch_data.get('patterns', [])
        total_patterns_in += len(batch_patterns)

        for pattern in batch_patterns:
            name = pattern.get('name', '')
            chunk_ref = pattern.get('chunk_ref', '')
            quote = pattern.get('quote', '')
            description = pattern.get('description', '')

            # Build source entry
            source = {
                'chunk_ref': chunk_ref,
                'quote': quote
            }

            # Find matching existing pattern
            match_key, similarity = find_matching_pattern(name, patterns)

            if match_key:
                # Merge into existing pattern
                patterns[match_key]['sources'].append(source)
                # Keep longest description
                if len(description) > len(patterns[match_key].get('description', '')):
                    patterns[match_key]['description'] = description
            else:
                # New pattern
                patterns[name] = {
                    'name': name,
                    'sources': [source],
                    'description': description
                }

    # Build output structure
    output_patterns = []
    for name, data in patterns.items():
        # Merge sources info into description
        source_count = len(data['sources'])
        merged_desc = data.get('description', '')
        if source_count > 1:
            merged_desc = f"Merged from {source_count} sources. {merged_desc}"

        output_patterns.append({
            'name': data['name'],
            'sources': data['sources'],
            'description': merged_desc
        })

    return {
        'field': field_name,
        'aggregated_at': datetime.now().isoformat(),
        'batches_merged': batches_merged,
        'patterns_input': total_patterns_in,
        'patterns_output': len(output_patterns),
        'patterns': output_patterns
    }


def main():
    parser = argparse.ArgumentParser(
        description='Aggregate patterns from batch extractions (Level 6 of 7-Level Architecture)'
    )
    parser.add_argument('project_path', type=Path, help='Path to research project')
    parser.add_argument('--input-dir', '-i', type=Path, required=True, help='Directory with batch YAML files')
    parser.add_argument('--output-dir', '-o', type=Path, required=True, help='Output directory for aggregated files')
    args = parser.parse_args()

    project_path = args.project_path
    if not project_path.is_absolute():
        project_path = Path.cwd() / project_path

    # Resolve paths
    input_dir = args.input_dir
    if not input_dir.is_absolute():
        input_dir = project_path / input_dir

    output_dir = args.output_dir
    if not output_dir.is_absolute():
        output_dir = project_path / output_dir

    if not input_dir.exists():
        print(f"ERROR: Input directory not found: {input_dir}", file=sys.stderr)
        sys.exit(1)

    # Find batch files
    batch_files = list(input_dir.glob('_batch_*.yaml'))
    if not batch_files:
        print(f"ERROR: No batch files found in {input_dir}", file=sys.stderr)
        sys.exit(1)

    # Discover fields from batch files
    fields = set()
    for batch_path in batch_files:
        batch_data = load_yaml(batch_path)
        if 'field' in batch_data:
            fields.add(batch_data['field'])

    print(f"Found {len(batch_files)} batch files across {len(fields)} fields")

    # Aggregate each field
    output_dir.mkdir(parents=True, exist_ok=True)

    total_in = 0
    total_out = 0

    for field_name in sorted(fields):
        print(f"\nAggregating field: {field_name}")
        result = aggregate_field(batch_files, field_name)

        total_in += result['patterns_input']
        total_out += result['patterns_output']

        dedup_rate = (1 - result['patterns_output'] / result['patterns_input']) * 100 if result['patterns_input'] > 0 else 0

        print(f"  Batches: {result['batches_merged']}")
        print(f"  Patterns: {result['patterns_input']} -> {result['patterns_output']} ({dedup_rate:.0f}% dedup)")

        # Write output
        output_path = output_dir / f"_synthesis_{field_name}.yaml"
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(result, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    # Summary
    overall_dedup = (1 - total_out / total_in) * 100 if total_in > 0 else 0

    print(f"\n{'='*50}")
    print(f"Level 6 Complete: Aggregation")
    print(f"{'='*50}")
    print(f"Total patterns: {total_in} -> {total_out} ({overall_dedup:.0f}% deduplication)")
    print(f"Output files: {output_dir}/_synthesis_*.yaml")


if __name__ == '__main__':
    main()
