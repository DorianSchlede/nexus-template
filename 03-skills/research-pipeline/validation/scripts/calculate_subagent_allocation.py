#!/usr/bin/env python3
"""
calculate_subagent_allocation.py - Level 2 of 7-Level Synthesis Architecture

Calculates subagent batch allocation using greedy bin-packing with token budgets.
Also calculates Level 7 token budget (Gap G2 Fix).

Uses standard token formula: chars // 4 (Gap G3).

Usage:
    python calculate_subagent_allocation.py PROJECT_PATH --input ROUTING_FILE --output PLAN_FILE
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple
import yaml
from math import ceil


# Standard token formula (Gap G3)
def estimate_tokens(chars: int) -> int:
    """Standard token estimation: chars // 4."""
    return chars // 4


# Budget constants
TOKEN_BUDGET_PER_BATCH = 70000  # Level 4 extraction batches
METHODOLOGY_TOKENS = 3000
BRIEFING_TOKENS = 2050  # Includes research_purpose buffer
OUTPUT_RESERVATION = 20000
TOTAL_CONTEXT = 100000
MAX_SYNTHESIS_INPUT = 75000  # Before requiring split


def load_routing(routing_path: Path) -> Dict[str, Any]:
    """Load synthesis routing table."""
    with open(routing_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def greedy_bin_pack(chunks: List[Dict], budget: int) -> List[List[Dict]]:
    """
    Greedy bin-packing algorithm for chunks into batches.

    Groups chunks by paper when possible, respects token budget.
    """
    if not chunks:
        return []

    # Sort by paper_id to keep paper chunks together
    chunks_sorted = sorted(chunks, key=lambda c: (c['paper_id'], c['chunk']))

    batches = []
    current_batch = []
    current_tokens = 0

    for chunk in chunks_sorted:
        chunk_tokens = chunk.get('token_count', 10000)  # Default 10k if unknown

        # Check if adding this chunk would exceed budget
        if current_tokens + chunk_tokens > budget and current_batch:
            # Start new batch
            batches.append(current_batch)
            current_batch = [chunk]
            current_tokens = chunk_tokens
        else:
            # Add to current batch
            current_batch.append(chunk)
            current_tokens += chunk_tokens

    # Don't forget the last batch
    if current_batch:
        batches.append(current_batch)

    return batches


def calculate_level7_budget(field_count: int, avg_patterns_per_field: int = 25) -> Dict[str, Any]:
    """
    Calculate token budget for Level 7 final report subagent.

    Estimates synthesis file sizes based on field count and pattern estimates.
    """
    # Estimate: each field synthesis ~3000 tokens (patterns + metadata)
    estimated_tokens_per_field = 3000
    synthesis_files_estimated = field_count * estimated_tokens_per_field

    usable = TOTAL_CONTEXT - METHODOLOGY_TOKENS - BRIEFING_TOKENS - OUTPUT_RESERVATION - synthesis_files_estimated

    requires_split = usable < 10000 or synthesis_files_estimated > MAX_SYNTHESIS_INPUT

    return {
        'methodology': METHODOLOGY_TOKENS,
        'briefing': BRIEFING_TOKENS,
        'synthesis_files_estimated': synthesis_files_estimated,
        'output_reservation': OUTPUT_RESERVATION,
        'total_available': TOTAL_CONTEXT,
        'usable': max(0, usable),
        'requires_split': requires_split,
        'split_strategy': 'group_by_priority' if requires_split else None
    }


def calculate_allocation(routing: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate subagent allocation from routing table.

    Returns subagent plan with batch assignments and Level 7 budget.
    """
    allocation = {
        'project': routing['project'],
        'generated_at': datetime.now().isoformat(),
        'token_budget_per_batch': TOKEN_BUDGET_PER_BATCH,
        'standard_formula': 'chars // 4',
        'level4_batches': [],
        'level7_budget': {},
        'stats': {
            'total_batches': 0,
            'max_concurrent': 15,
            'estimated_total_time': ''
        }
    }

    batch_id = 0
    total_batches = 0

    # Process each field
    for field_name, field_data in routing['fields'].items():
        chunks = field_data.get('chunks', [])

        if not chunks:
            continue

        # Bin-pack chunks into batches
        batches = greedy_bin_pack(chunks, TOKEN_BUDGET_PER_BATCH)

        for i, batch_chunks in enumerate(batches, 1):
            batch_id += 1
            total_tokens = sum(c.get('token_count', 10000) for c in batch_chunks)

            # Estimate duration: ~1min per 15k tokens
            estimated_mins = max(1, total_tokens // 15000)

            allocation['level4_batches'].append({
                'batch_id': f"{field_name}_{i}",
                'field': field_name,
                'chunks': batch_chunks,
                'total_tokens': total_tokens,
                'estimated_duration': f"{estimated_mins} min"
            })

        total_batches += len(batches)

    # Calculate Level 7 budget
    field_count = len(routing['fields'])
    allocation['level7_budget'] = calculate_level7_budget(field_count)

    # Update stats
    allocation['stats']['total_batches'] = total_batches

    # Estimate total time: batches / 15 concurrent × avg 3 min
    if total_batches > 0:
        parallel_rounds = ceil(total_batches / 15)
        estimated_total_mins = parallel_rounds * 3
        allocation['stats']['estimated_total_time'] = f"{estimated_total_mins} min"

    return allocation


def main():
    parser = argparse.ArgumentParser(
        description='Calculate subagent allocation with token budgets (Level 2 of 7-Level Architecture)'
    )
    parser.add_argument('project_path', type=Path, help='Path to research project')
    parser.add_argument('--input', '-i', type=Path, required=True, help='Input routing YAML file')
    parser.add_argument('--output', '-o', type=Path, required=True, help='Output subagent plan YAML file')
    args = parser.parse_args()

    project_path = args.project_path
    if not project_path.is_absolute():
        project_path = Path.cwd() / project_path

    # Resolve input path
    input_path = args.input
    if not input_path.is_absolute():
        input_path = project_path / input_path

    if not input_path.exists():
        print(f"ERROR: Routing file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Load routing
    print(f"Loading routing from {input_path}...")
    routing = load_routing(input_path)

    # Calculate allocation
    print("Calculating subagent allocation...")
    allocation = calculate_allocation(routing)

    # Write output
    output_path = args.output
    if not output_path.is_absolute():
        output_path = project_path / output_path

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(allocation, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"\nLevel 2 Complete: Subagent plan written to {output_path}")
    print(f"  Total batches: {allocation['stats']['total_batches']}")
    print(f"  Max concurrent: {allocation['stats']['max_concurrent']}")
    print(f"  Estimated time: {allocation['stats']['estimated_total_time']}")

    # Report Level 7 budget
    l7 = allocation['level7_budget']
    print(f"\nLevel 7 Token Budget (Gap G2):")
    print(f"  Synthesis files: ~{l7['synthesis_files_estimated']:,} tokens")
    print(f"  Usable: {l7['usable']:,} tokens")
    print(f"  Requires split: {'Yes' if l7['requires_split'] else 'No'}")


if __name__ == '__main__':
    main()
