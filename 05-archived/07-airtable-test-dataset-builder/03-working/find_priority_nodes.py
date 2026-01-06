#!/usr/bin/env python3
"""
Find Priority Nodes for MetaTuner Testing

Criteria:
- Task accuracy between 60% and 99%
- At least 50 tasks total
- At least 10 failed tasks (<80% accuracy)
- Latest NodeVersion only

Usage:
    python find_priority_nodes.py [OPTIONS]

Options:
    --min-accuracy FLOAT    Minimum task accuracy (default: 60.0)
    --max-accuracy FLOAT    Maximum task accuracy (default: 99.0)
    --min-tasks INT         Minimum total tasks (default: 50)
    --min-failed INT        Minimum failed tasks <80% (default: 10)
    --output PATH           Output JSON file path
    --verbose               Show detailed progress

Output: JSON with priority nodes meeting all criteria
"""

import os
import sys
import csv
import json
import argparse
from datetime import datetime
from collections import defaultdict

# Increase CSV field size limit
csv.field_size_limit(sys.maxsize)

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
RESOURCES_DIR = os.path.join(PROJECT_DIR, '02-resources')
OUTPUT_DIR = os.path.join(PROJECT_DIR, '04-outputs')


def load_csv(filename):
    """Load CSV file into list of dicts."""
    filepath = os.path.join(RESOURCES_DIR, filename)
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    records = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    return records


def parse_date(date_str):
    """Parse date string to datetime, return None if invalid."""
    if not date_str or date_str == 'Unknown':
        return None
    try:
        # Handle various formats
        for fmt in ['%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S']:
            try:
                return datetime.strptime(date_str.split('.')[0].split('Z')[0], fmt)
            except ValueError:
                continue
        return None
    except:
        return None


def find_latest_node_versions(node_tasks, verbose=False):
    """
    Find the latest NodeVersion for each Node based on NodeTask data.

    Returns: dict of {node_name: {version_id, version_date, node_tasks}}
    """
    if verbose:
        print("Finding latest NodeVersion per Node...")

    # Group NodeTasks by Node name
    node_data = defaultdict(lambda: defaultdict(list))

    for nt in node_tasks:
        # Use actual column names from CSV
        node_name = nt.get('Name (from Node)', '').strip()
        version_id = nt.get('Node Version', '').strip()
        created_at = nt.get('Record Created At', '') or nt.get('CreatedTime', '')
        created_at = created_at.strip() if created_at else ''

        if node_name and version_id:
            node_data[node_name][version_id].append({
                'task': nt,
                'created_at': parse_date(created_at),
                'created_at_str': created_at
            })

    # For each node, find the version with the most recent created_at
    latest_versions = {}

    for node_name, versions in node_data.items():
        latest_version = None
        latest_date = None
        latest_date_str = 'Unknown'

        for version_id, tasks in versions.items():
            # Get the max date for this version
            version_dates = [t['created_at'] for t in tasks if t['created_at']]
            if version_dates:
                max_date = max(version_dates)
                if latest_date is None or max_date > latest_date:
                    latest_date = max_date
                    latest_version = version_id
                    latest_date_str = tasks[0]['created_at_str']
            elif latest_version is None:
                # No dates, use first version found
                latest_version = version_id

        if latest_version:
            latest_versions[node_name] = {
                'version_id': latest_version,
                'version_date': latest_date_str,
                'node_tasks': [t['task'] for t in versions[latest_version]]
            }

    if verbose:
        print(f"  Found {len(latest_versions)} nodes with version data")

    return latest_versions


def calculate_node_stats(latest_versions, variable_tasks, verbose=False):
    """
    Calculate accuracy stats for each node using only latest version.
    Uses TaskNodeAccuracy directly from NodeTasks.

    Returns: list of node stats dicts
    """
    if verbose:
        print("Calculating accuracy stats per node...")

    node_stats = []

    for node_name, version_data in latest_versions.items():
        node_tasks_list = version_data['node_tasks']

        # Collect all accuracies for tasks of this node version
        # Use TaskNodeAccuracy directly from NodeTask (format: "91%")
        task_accuracies = []

        for nt in node_tasks_list:
            acc_str = nt.get('TaskNodeAccuracy', '').strip()
            if acc_str and acc_str != 'NaN':
                # Parse "91%" to 91.0
                try:
                    acc = float(acc_str.replace('%', ''))
                    task_accuracies.append(acc)
                except ValueError:
                    pass

        if not task_accuracies:
            continue

        # Calculate stats
        avg_accuracy = sum(task_accuracies) / len(task_accuracies)
        failed_tasks = sum(1 for a in task_accuracies if a < 80)
        passed_tasks = sum(1 for a in task_accuracies if a >= 80)

        # Get agent from first node task - use actual column name
        agent = ''
        if node_tasks_list:
            agent = node_tasks_list[0].get('Agent (from Node)', '').strip()

        # Count variable tasks for this node (from NodeTasks.TotalVariableTasks)
        total_vars = 0
        for nt in node_tasks_list:
            try:
                total_vars += int(nt.get('TotalVariableTasks', 0) or 0)
            except (ValueError, TypeError):
                pass

        node_stats.append({
            'node': node_name,
            'agent': agent,
            'latest_version_id': version_data['version_id'],
            'latest_version_date': version_data['version_date'],
            'total_tasks': len(task_accuracies),
            'failed_tasks': failed_tasks,
            'passed_tasks': passed_tasks,
            'avg_accuracy': round(avg_accuracy, 2),
            'total_variables': total_vars
        })

    # Sort by total_tasks descending
    node_stats.sort(key=lambda x: x['total_tasks'], reverse=True)

    if verbose:
        print(f"  Calculated stats for {len(node_stats)} nodes")

    return node_stats


def filter_priority_nodes(node_stats, min_accuracy=60.0, max_accuracy=99.0,
                          min_tasks=50, min_failed=10, verbose=False):
    """
    Filter nodes by priority criteria.

    Criteria:
    - avg_accuracy between min_accuracy and max_accuracy
    - total_tasks >= min_tasks
    - failed_tasks >= min_failed
    """
    if verbose:
        print(f"\nFiltering by criteria:")
        print(f"  Accuracy: {min_accuracy}% - {max_accuracy}%")
        print(f"  Min tasks: {min_tasks}")
        print(f"  Min failed tasks (<80%): {min_failed}")

    priority_nodes = []

    for node in node_stats:
        if (min_accuracy <= node['avg_accuracy'] <= max_accuracy and
            node['total_tasks'] >= min_tasks and
            node['failed_tasks'] >= min_failed):
            priority_nodes.append(node)

    if verbose:
        print(f"\n  Found {len(priority_nodes)} priority nodes")

    return priority_nodes


def main():
    parser = argparse.ArgumentParser(description='Find priority nodes for MetaTuner testing')
    parser.add_argument('--min-accuracy', type=float, default=60.0,
                        help='Minimum task accuracy (default: 60.0)')
    parser.add_argument('--max-accuracy', type=float, default=99.0,
                        help='Maximum task accuracy (default: 99.0)')
    parser.add_argument('--min-tasks', type=int, default=50,
                        help='Minimum total tasks (default: 50)')
    parser.add_argument('--min-failed', type=int, default=10,
                        help='Minimum failed tasks <80% (default: 10)')
    parser.add_argument('--output', '-o', help='Output JSON file path')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed progress')
    args = parser.parse_args()

    # Load data
    if args.verbose:
        print("Loading CSV data...")

    node_tasks = load_csv('NodeTasks-ALL.csv')
    variable_tasks = load_csv('VariableTasks-WithExpected.csv')

    if args.verbose:
        print(f"  Loaded {len(node_tasks)} NodeTasks")
        print(f"  Loaded {len(variable_tasks)} VariableTasks")

    # Find latest versions
    latest_versions = find_latest_node_versions(node_tasks, args.verbose)

    # Calculate stats
    node_stats = calculate_node_stats(latest_versions, variable_tasks, args.verbose)

    # Filter priority nodes
    priority_nodes = filter_priority_nodes(
        node_stats,
        min_accuracy=args.min_accuracy,
        max_accuracy=args.max_accuracy,
        min_tasks=args.min_tasks,
        min_failed=args.min_failed,
        verbose=args.verbose
    )

    # Output
    output = {
        'generated_at': datetime.now().isoformat(),
        'criteria': {
            'min_accuracy': args.min_accuracy,
            'max_accuracy': args.max_accuracy,
            'min_tasks': args.min_tasks,
            'min_failed': args.min_failed
        },
        'total_nodes_analyzed': len(node_stats),
        'priority_nodes_found': len(priority_nodes),
        'priority_nodes': priority_nodes,
        'all_nodes': node_stats  # Include all for reference
    }

    # Save output
    if args.output:
        output_path = args.output
    else:
        output_path = os.path.join(OUTPUT_DIR, 'priority-nodes.json')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    # Print summary
    print("\n" + "=" * 70)
    print("PRIORITY NODES FOR METATUNER TESTING")
    print("=" * 70)
    print(f"\nCriteria: {args.min_accuracy}%-{args.max_accuracy}% accuracy, "
          f">={args.min_tasks} tasks, >={args.min_failed} failed")
    print(f"\nNodes analyzed: {len(node_stats)}")
    print(f"Priority nodes found: {len(priority_nodes)}")

    if priority_nodes:
        print("\n" + "-" * 70)
        print(f"{'Node':<45} {'Agent':<20} {'Tasks':>6} {'Failed':>7} {'Acc%':>6}")
        print("-" * 70)
        for node in priority_nodes:
            node_short = node['node'][:43] + '..' if len(node['node']) > 45 else node['node']
            agent_short = node['agent'][:18] + '..' if len(node['agent']) > 20 else node['agent']
            print(f"{node_short:<45} {agent_short:<20} {node['total_tasks']:>6} "
                  f"{node['failed_tasks']:>7} {node['avg_accuracy']:>5.1f}%")
    else:
        print("\nNo nodes match the criteria. Consider relaxing parameters.")
        print("\nTop 10 nodes by task count:")
        print("-" * 70)
        for node in node_stats[:10]:
            node_short = node['node'][:43] + '..' if len(node['node']) > 45 else node['node']
            print(f"  {node_short}: {node['total_tasks']} tasks, "
                  f"{node['failed_tasks']} failed, {node['avg_accuracy']:.1f}%")

    print(f"\nOutput saved to: {output_path}")


if __name__ == '__main__':
    main()
