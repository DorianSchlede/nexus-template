#!/usr/bin/env python3
"""
Airtable Test Dataset Inventory

Queries Airtable to build a comprehensive inventory of:
- Workspaces and Agents
- DatasetVariables (Expected Values)
- Accuracy distribution
- Link integrity validation

Usage:
    python inventory.py [--output PATH] [--verbose]

Output:
    04-outputs/inventory-report.json
"""

import os
import sys
import json
import argparse
from datetime import datetime
from collections import defaultdict
import urllib.parse

# Find Nexus root
def find_nexus_root():
    current = os.path.dirname(os.path.abspath(__file__))
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, 'CLAUDE.md')):
            return current
        current = os.path.dirname(current)
    return None

NEXUS_ROOT = find_nexus_root()
if not NEXUS_ROOT:
    print("Error: Could not find Nexus root")
    sys.exit(1)

sys.path.insert(0, NEXUS_ROOT)

try:
    import requests
except ImportError:
    print("Error: Missing 'requests' library")
    print("   Run: pip install requests")
    sys.exit(1)


# ============================================================================
# Configuration
# ============================================================================

API_BASE_URL = 'https://api.airtable.com/v0'
BASE_ID = 'appFPoOfBpUv73M5A'

# Table IDs from query-guide.md
TABLES = {
    'Agents': 'tblVEJD2inVhae855',
    'Nodes': 'tblPJ9VKG74mKv7JK',
    'NodeVersions': 'tblh0GsN5Et3ApzLS',
    'Variables': 'tblf2ohTHmsucjVUj',
    'AgentTasks': 'tblsEzGhn4XJjNrkt',
    'NodeTasks': 'tblNdPnVWDragZtcK',
    'VariableTasks': 'tblKhpqLs06kI01yv',
    'Datasets': 'tbltUrvSBnfOb4S8v',
    'DatasetTasks': 'tbl9lACSI4fDUzAv4',
    'DatasetNodes': 'tblflNTX3tR0onX13',
    'DatasetVariables': 'tblsHYj8CrdHbY8Bt',
}


# ============================================================================
# API Helpers
# ============================================================================

def load_env():
    """Load .env file."""
    env_path = os.path.join(NEXUS_ROOT, '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip().strip('"\'')


def get_headers():
    """Get API headers."""
    api_key = os.environ.get('AIRTABLE_API_KEY')
    if not api_key:
        raise ValueError("AIRTABLE_API_KEY not set in environment or .env")
    return {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }


def query_table(table_name, filter_formula=None, fields=None, limit=None, verbose=False):
    """Query all records from a table with pagination."""
    table_id = TABLES.get(table_name)
    if not table_id:
        raise ValueError(f"Unknown table: {table_name}")

    headers = get_headers()
    records = []
    url = f"{API_BASE_URL}/{BASE_ID}/{table_id}"
    offset = None

    while True:
        params = {'pageSize': 100}

        if offset:
            params['offset'] = offset
        if filter_formula:
            params['filterByFormula'] = filter_formula
        if fields:
            for field in fields:
                params.setdefault('fields[]', []).append(field)

        if verbose:
            print(f"   Fetching {table_name}... (offset: {offset or 'start'})")

        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)

            if response.status_code == 422:
                error = response.json().get('error', {})
                print(f"Error querying {table_name}: {error.get('message', 'Unknown')}")
                return records

            if response.status_code != 200:
                print(f"Error querying {table_name}: HTTP {response.status_code}")
                return records

            data = response.json()
            batch = data.get('records', [])
            records.extend(batch)

            if limit and len(records) >= limit:
                records = records[:limit]
                break

            offset = data.get('offset')
            if not offset:
                break

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            break

    return records


def count_records(table_name, filter_formula=None, verbose=False):
    """Count records matching a filter without fetching all data."""
    # Airtable doesn't have a COUNT endpoint, so we fetch with minimal fields
    records = query_table(
        table_name,
        filter_formula=filter_formula,
        fields=['Created'],  # Minimal field to reduce payload
        verbose=verbose
    )
    return len(records)


# ============================================================================
# Inventory Functions
# ============================================================================

def get_agents_inventory(verbose=False):
    """Get all agents with their workspace info."""
    if verbose:
        print("\n[1/5] Fetching Agents...")

    agents = query_table(
        'Agents',
        fields=['Agent Name', 'Workspace', 'Nodes'],
        verbose=verbose
    )

    result = []
    for agent in agents:
        fields = agent.get('fields', {})
        result.append({
            'id': agent['id'],
            'name': fields.get('Agent Name', 'Unnamed'),
            'workspace': fields.get('Workspace', []),
            'nodes_count': len(fields.get('Nodes', []))
        })

    return result


def get_dataset_variables_inventory(verbose=False, limit=None):
    """Get DatasetVariables with Expected Value and linked data."""
    if verbose:
        print("\n[2/5] Fetching DatasetVariables with Expected Values...")

    # Fetch DatasetVariables with Expected Value
    records = query_table(
        'DatasetVariables',
        filter_formula="{Expected Value}!=BLANK()",
        fields=[
            'Variable Name',
            'Expected Value',
            'Expected Value Status',
            'DatasetNodes',
            'OriginalVariableTask',
            'Agent (from OriginalAgentTask)'
        ],
        limit=limit,
        verbose=verbose
    )

    return records


def get_variable_tasks_with_accuracy(verbose=False, limit=None):
    """Get VariableTasks that have DatasetVariable links (for accuracy stats)."""
    if verbose:
        print("\n[3/5] Fetching VariableTasks with Accuracy data...")

    records = query_table(
        'VariableTasks',
        filter_formula="{DatasetVariable}!=BLANK()",
        fields=[
            'VariableTask Name',
            'AIValue',
            'Accuracy',
            'VariableTaskAccuracy',
            'Variable Name',
            'DatasetVariable'
        ],
        limit=limit,
        verbose=verbose
    )

    return records


def get_dataset_nodes_inventory(verbose=False, limit=None):
    """Get DatasetNodes with NodeVersion links."""
    if verbose:
        print("\n[4/5] Fetching DatasetNodes...")

    records = query_table(
        'DatasetNodes',
        fields=['DatasetNode Name', 'Node Version (from NodeTask)', 'NodeTask'],
        limit=limit,
        verbose=verbose
    )

    return records


def get_dataset_tasks_inventory(verbose=False):
    """Get DatasetTasks."""
    if verbose:
        print("\n[5/5] Fetching DatasetTasks...")

    # Query with minimal fields
    records = query_table(
        'DatasetTasks',
        fields=['DatasetTask Name', 'Dataset'],
        verbose=verbose
    )

    return records


# ============================================================================
# Aggregation Functions
# ============================================================================

def aggregate_by_agent(dataset_vars):
    """Aggregate DatasetVariables by Agent."""
    by_agent = defaultdict(lambda: {
        'count': 0,
        'variables': set(),
        'record_ids': []
    })

    for record in dataset_vars:
        fields = record.get('fields', {})
        agents = fields.get('Agent (from OriginalAgentTask)', [])
        var_name = fields.get('Variable Name', 'Unknown')

        for agent in agents if agents else ['Unknown']:
            by_agent[agent]['count'] += 1
            by_agent[agent]['variables'].add(var_name)
            by_agent[agent]['record_ids'].append(record['id'])

    # Convert sets to counts
    result = {}
    for agent, data in by_agent.items():
        result[agent] = {
            'expected_value_count': data['count'],
            'unique_variables': len(data['variables']),
            'variable_names': list(data['variables'])[:10]  # Sample
        }

    return result


def calculate_accuracy_distribution(variable_tasks):
    """Calculate accuracy distribution from VariableTasks."""
    distribution = {
        'perfect': 0,      # accuracy = 1.0
        'high': 0,         # 0.8 <= accuracy < 1.0
        'medium': 0,       # 0.5 <= accuracy < 0.8
        'low': 0,          # 0.1 <= accuracy < 0.5
        'failed': 0,       # accuracy = 0
        'unknown': 0       # no accuracy value
    }

    accuracy_values = []

    for record in variable_tasks:
        fields = record.get('fields', {})
        accuracy = fields.get('VariableTaskAccuracy')

        if accuracy is None:
            distribution['unknown'] += 1
        elif accuracy == 1:
            distribution['perfect'] += 1
            accuracy_values.append(1.0)
        elif accuracy == 0:
            distribution['failed'] += 1
            accuracy_values.append(0.0)
        elif accuracy >= 0.8:
            distribution['high'] += 1
            accuracy_values.append(accuracy)
        elif accuracy >= 0.5:
            distribution['medium'] += 1
            accuracy_values.append(accuracy)
        else:
            distribution['low'] += 1
            accuracy_values.append(accuracy)

    avg_accuracy = sum(accuracy_values) / len(accuracy_values) if accuracy_values else 0

    return {
        'distribution': distribution,
        'total': len(variable_tasks),
        'with_accuracy': len(accuracy_values),
        'average_accuracy': round(avg_accuracy, 3)
    }


def validate_links(dataset_vars, dataset_nodes, verbose=False):
    """Validate link integrity between tables."""
    if verbose:
        print("\n[Validating] Link integrity...")

    # Check DatasetVariables → DatasetNodes links
    vars_with_nodes = 0
    vars_without_nodes = 0

    for record in dataset_vars:
        fields = record.get('fields', {})
        nodes = fields.get('DatasetNodes', [])
        if nodes:
            vars_with_nodes += 1
        else:
            vars_without_nodes += 1

    # Check DatasetNodes → NodeVersion links (via NodeTask lookup)
    nodes_with_version = 0
    nodes_without_version = 0

    for record in dataset_nodes:
        fields = record.get('fields', {})
        version = fields.get('Node Version (from NodeTask)', [])
        if version:
            nodes_with_version += 1
        else:
            nodes_without_version += 1

    return {
        'dataset_variables': {
            'with_dataset_nodes': vars_with_nodes,
            'without_dataset_nodes': vars_without_nodes,
            'link_rate': round(vars_with_nodes / (vars_with_nodes + vars_without_nodes), 3) if (vars_with_nodes + vars_without_nodes) > 0 else 0
        },
        'dataset_nodes': {
            'with_node_version': nodes_with_version,
            'without_node_version': nodes_without_version,
            'link_rate': round(nodes_with_version / (nodes_with_version + nodes_without_version), 3) if (nodes_with_version + nodes_without_version) > 0 else 0
        }
    }


# ============================================================================
# Main
# ============================================================================

def build_inventory(verbose=False, quick=False):
    """Build complete inventory report."""
    print("=" * 60)
    print("Airtable Test Dataset Inventory")
    if quick:
        print("(QUICK MODE - Limited to 500 records per table)")
    print("=" * 60)

    # Load environment
    load_env()

    limit = 500 if quick else None

    # Fetch data - pass limit to query functions directly
    agents = get_agents_inventory(verbose)
    dataset_vars = get_dataset_variables_inventory(verbose, limit=limit)
    variable_tasks = get_variable_tasks_with_accuracy(verbose, limit=limit)
    dataset_nodes = get_dataset_nodes_inventory(verbose, limit=limit)
    dataset_tasks = get_dataset_tasks_inventory(verbose)

    # Aggregate
    by_agent = aggregate_by_agent(dataset_vars)
    accuracy_stats = calculate_accuracy_distribution(variable_tasks)
    link_validation = validate_links(dataset_vars, dataset_nodes, verbose)

    # Build report
    report = {
        'generated_at': datetime.now().isoformat(),
        'base_id': BASE_ID,
        'summary': {
            'total_agents': len(agents),
            'total_dataset_variables_with_expected': len(dataset_vars),
            'total_variable_tasks_with_dataset_link': len(variable_tasks),
            'total_dataset_nodes': len(dataset_nodes),
            'total_dataset_tasks_expected_done': len(dataset_tasks)
        },
        'accuracy_stats': accuracy_stats,
        'by_agent': by_agent,
        'link_validation': link_validation,
        'agents': agents
    }

    return report


def main():
    parser = argparse.ArgumentParser(description='Build Airtable test dataset inventory')
    parser.add_argument('--output', '-o', default=None, help='Output file path')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed progress')
    parser.add_argument('--quick', '-q', action='store_true', help='Quick mode - limit to 500 records per table')
    args = parser.parse_args()

    # Build inventory
    report = build_inventory(verbose=args.verbose, quick=args.quick)

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(project_dir, '04-outputs')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'inventory-report.json')

    # Write report
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Print summary
    print("\n" + "=" * 60)
    print("INVENTORY SUMMARY")
    print("=" * 60)
    print(f"Agents:                          {report['summary']['total_agents']}")
    print(f"DatasetVariables (with Expected): {report['summary']['total_dataset_variables_with_expected']}")
    print(f"VariableTasks (with Dataset link): {report['summary']['total_variable_tasks_with_dataset_link']}")
    print(f"DatasetNodes:                    {report['summary']['total_dataset_nodes']}")
    print(f"DatasetTasks (Expected Done):    {report['summary']['total_dataset_tasks_expected_done']}")
    print()
    print("ACCURACY DISTRIBUTION:")
    dist = report['accuracy_stats']['distribution']
    print(f"  Perfect (1.0):  {dist['perfect']}")
    print(f"  High (>=0.8):   {dist['high']}")
    print(f"  Medium (>=0.5): {dist['medium']}")
    print(f"  Low (<0.5):     {dist['low']}")
    print(f"  Failed (0):     {dist['failed']}")
    print(f"  Unknown:        {dist['unknown']}")
    print(f"  Average:        {report['accuracy_stats']['average_accuracy']}")
    print()
    print("LINK VALIDATION:")
    lv = report['link_validation']
    print(f"  DatasetVariables -> DatasetNodes: {lv['dataset_variables']['link_rate']*100:.1f}%")
    print(f"  DatasetNodes -> NodeVersion:      {lv['dataset_nodes']['link_rate']*100:.1f}%")
    print()
    print(f"Report saved to: {output_path}")


if __name__ == '__main__':
    main()
