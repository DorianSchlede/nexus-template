#!/usr/bin/env python3
"""
MetaTuner Dataset Export

Exports Airtable test data to MetaTuner-compatible format.

Usage:
    python export_dataset.py [OPTIONS]

Options:
    --agent NAME       Filter by agent name (partial match)
    --tier TIER        Quality tier: gold, silver, bronze (default: gold)
    --limit N          Max records to export
    --output PATH      Output file path
    --format FORMAT    Output format: json, jsonl (default: json)
    --verbose          Show detailed progress

Examples:
    python export_dataset.py --agent "Deal Breaker" --tier gold
    python export_dataset.py --agent "TZV" --limit 100 --format jsonl
"""

import os
import sys
import csv
import json
import argparse
from datetime import datetime
from collections import defaultdict

# Increase CSV field size limit for large cells
csv.field_size_limit(sys.maxsize)

# Find project root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
RESOURCES_DIR = os.path.join(PROJECT_DIR, '02-resources')
OUTPUT_DIR = os.path.join(PROJECT_DIR, '04-outputs', 'datasets')


# ============================================================================
# Data Loading
# ============================================================================

def load_csv(filename, key_field=None):
    """Load CSV file into list of dicts or dict keyed by field."""
    filepath = os.path.join(RESOURCES_DIR, filename)
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    records = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)

    if key_field:
        # Return as dict keyed by field
        return {r.get(key_field, ''): r for r in records if r.get(key_field)}

    return records


def load_all_data(verbose=False):
    """Load all CSV data files."""
    if verbose:
        print("Loading CSV data...")

    data = {}

    if verbose:
        print("  Loading DatasetVariables...")
    data['dataset_variables'] = load_csv('DatasetVariables-FULL.csv')

    if verbose:
        print("  Loading VariableTasks...")
    data['variable_tasks'] = load_csv('VariableTasks-WithExpected.csv')

    if verbose:
        print("  Loading DatasetNodes...")
    data['dataset_nodes'] = load_csv('DatasetNodes-ALL.csv')

    if verbose:
        print("  Loading NodeTasks...")
    data['node_tasks'] = load_csv('NodeTasks-ALL.csv')

    if verbose:
        print(f"  Loaded: {len(data['dataset_variables'])} DatasetVariables")
        print(f"  Loaded: {len(data['variable_tasks'])} VariableTasks")
        print(f"  Loaded: {len(data['dataset_nodes'])} DatasetNodes")
        print(f"  Loaded: {len(data['node_tasks'])} NodeTasks")

    return data


# ============================================================================
# Filtering
# ============================================================================

def filter_by_agent(records, agent_name):
    """Filter records by agent name (partial match, case-insensitive)."""
    agent_lower = agent_name.lower()
    return [r for r in records if agent_lower in r.get('Agent (from OriginalAgentTask)', '').lower()]


def filter_by_tier(records, tier):
    """Filter records by quality tier."""
    if tier == 'gold':
        # Human reviewed
        return [r for r in records if r.get('Review', '').strip() == '1']
    elif tier == 'silver':
        # Status = Done
        return [r for r in records if r.get('Expected Output Status (from DatasetTask)', '').strip() == 'Done']
    elif tier == 'bronze':
        # Has expected value
        return [r for r in records if r.get('Expected Value', '').strip()]
    else:
        return records


def filter_with_expected(records):
    """Filter to only records with expected value."""
    return [r for r in records if r.get('Expected Value', '').strip()]


# ============================================================================
# Data Joining
# ============================================================================

def build_variable_task_index(variable_tasks):
    """Build index of VariableTasks by DatasetVariable ID."""
    index = defaultdict(list)
    for vt in variable_tasks:
        dv_id = vt.get('DatasetVariable', '').strip()
        if dv_id:
            index[dv_id].append(vt)
    return index


def build_node_task_index(node_tasks):
    """Build index of NodeTasks by NodeTask Name."""
    return {nt.get('NodeTask Name', ''): nt for nt in node_tasks}


def build_dataset_node_index(dataset_nodes):
    """Build index of DatasetNodes by DatasetNode Name."""
    return {dn.get('DatasetNode Name', ''): dn for dn in dataset_nodes}


# ============================================================================
# MetaTuner Format Transformation
# ============================================================================

def transform_to_metatuner(dataset_var, variable_tasks_idx, node_tasks_idx, dataset_nodes_idx):
    """Transform a DatasetVariable to MetaTuner format."""

    # Get the variable task for this dataset variable
    dv_uid = dataset_var.get('DatasetVariable UID', '')
    var_tasks = variable_tasks_idx.get(dv_uid, [])

    # Use the first matching variable task (or data from DatasetVariable)
    prompt = ''
    if var_tasks:
        vt = var_tasks[0]
        ai_value = vt.get('AIValue', '')
        accuracy = vt.get('VariableTaskAccuracy', '')
        # Get prompt directly from VariableTask (NodeTaskPrompt field)
        prompt = vt.get('NodeTaskPrompt', '')
        node_task_name = vt.get('NodeTask Name (from NodeTask)', '')
    else:
        # Fallback to lookup fields in DatasetVariable
        ai_value = dataset_var.get('AIValue (from OriginalVariableTask)', '')
        accuracy = dataset_var.get('VariableTaskAccuracy (from OriginalVariableTask)', '')
        node_task_name = ''

    # If no prompt from VariableTask, try via DatasetNodes -> NodeTask chain
    if not prompt:
        # Get DatasetNode name from DatasetVariable
        dataset_node_name = dataset_var.get('DatasetNodes', '').strip()
        if dataset_node_name and dataset_node_name in dataset_nodes_idx:
            dn = dataset_nodes_idx[dataset_node_name]
            # Get NodeTask ID from DatasetNode
            node_task_id = dn.get('NodeTask', '').strip()
            if node_task_id and node_task_id in node_tasks_idx:
                nt = node_tasks_idx[node_task_id]
                prompt = nt.get('Filled Prompt', '') or nt.get('Original Prompt Lookup', '')

    # Final fallback: direct NodeTask lookup by name
    if not prompt and node_task_name and node_task_name in node_tasks_idx:
        nt = node_tasks_idx[node_task_name]
        prompt = nt.get('Filled Prompt', '') or nt.get('Original Prompt Lookup', '')

    # Parse accuracy
    try:
        score = float(accuracy) if accuracy else None
    except (ValueError, TypeError):
        score = None

    # Build MetaTuner item
    item = {
        'variableName': dataset_var.get('Variable Name', ''),
        'expectedOutput': dataset_var.get('Expected Value', ''),
        'actualOutput': ai_value,
        'score': score,
        'prompt': prompt,
        'metadata': {
            'agent': dataset_var.get('Agent (from OriginalAgentTask)', ''),
            'datasetVariableUID': dv_uid,
            'reviewed': dataset_var.get('Review', '') == '1',
            'status': dataset_var.get('Expected Output Status (from DatasetTask)', ''),
        }
    }

    return item


# ============================================================================
# Export Functions
# ============================================================================

def export_dataset(data, agent=None, tier='gold', limit=None, verbose=False):
    """Export filtered dataset in MetaTuner format."""

    # Start with all dataset variables
    records = data['dataset_variables']

    if verbose:
        print(f"\nFiltering {len(records)} DatasetVariables...")

    # Filter by agent
    if agent:
        records = filter_by_agent(records, agent)
        if verbose:
            print(f"  After agent filter '{agent}': {len(records)}")

    # Filter to only those with expected values
    records = filter_with_expected(records)
    if verbose:
        print(f"  With expected value: {len(records)}")

    # Filter by quality tier
    records = filter_by_tier(records, tier)
    if verbose:
        print(f"  After tier filter '{tier}': {len(records)}")

    # Apply limit
    if limit and len(records) > limit:
        records = records[:limit]
        if verbose:
            print(f"  After limit: {len(records)}")

    if not records:
        print("No records match the filter criteria.")
        return []

    # Build indexes for joining
    if verbose:
        print("\nBuilding indexes...")
    vt_idx = build_variable_task_index(data['variable_tasks'])
    nt_idx = build_node_task_index(data['node_tasks'])
    dn_idx = build_dataset_node_index(data['dataset_nodes'])

    # Transform to MetaTuner format
    if verbose:
        print(f"\nTransforming {len(records)} records to MetaTuner format...")

    items = []
    for i, dv in enumerate(records):
        item = transform_to_metatuner(dv, vt_idx, nt_idx, dn_idx)
        items.append(item)

        if verbose and (i + 1) % 100 == 0:
            print(f"  Processed {i + 1}/{len(records)}")

    return items


def save_output(items, output_path, format='json'):
    """Save items to file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if format == 'jsonl':
        with open(output_path, 'w', encoding='utf-8') as f:
            for item in items:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
    else:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'generated_at': datetime.now().isoformat(),
                'count': len(items),
                'items': items
            }, f, indent=2, ensure_ascii=False)


# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description='Export Airtable data to MetaTuner format')
    parser.add_argument('--agent', '-a', help='Filter by agent name (partial match)')
    parser.add_argument('--tier', '-t', choices=['gold', 'silver', 'bronze'], default='gold',
                        help='Quality tier (default: gold)')
    parser.add_argument('--limit', '-l', type=int, help='Max records to export')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--format', '-f', choices=['json', 'jsonl'], default='json',
                        help='Output format (default: json)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed progress')
    args = parser.parse_args()

    # Load data
    data = load_all_data(args.verbose)

    # Export
    items = export_dataset(
        data,
        agent=args.agent,
        tier=args.tier,
        limit=args.limit,
        verbose=args.verbose
    )

    if not items:
        return

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        agent_slug = args.agent.lower().replace(' ', '-') if args.agent else 'all'
        filename = f"metatuner-{agent_slug}-{args.tier}.{args.format}"
        output_path = os.path.join(OUTPUT_DIR, filename)

    # Save
    save_output(items, output_path, args.format)

    # Summary
    print(f"\n{'=' * 60}")
    print("EXPORT SUMMARY")
    print('=' * 60)
    print(f"Records exported: {len(items)}")
    print(f"Agent filter: {args.agent or 'All'}")
    print(f"Quality tier: {args.tier}")
    print(f"Output format: {args.format}")
    print(f"Output file: {output_path}")

    # Stats
    with_prompt = sum(1 for i in items if i.get('prompt'))
    with_score = sum(1 for i in items if i.get('score') is not None)
    reviewed = sum(1 for i in items if i.get('metadata', {}).get('reviewed'))

    print(f"\nData quality:")
    print(f"  With prompt: {with_prompt} ({100*with_prompt/len(items):.1f}%)")
    print(f"  With score: {with_score} ({100*with_score/len(items):.1f}%)")
    print(f"  Reviewed: {reviewed} ({100*reviewed/len(items):.1f}%)")


if __name__ == '__main__':
    main()
