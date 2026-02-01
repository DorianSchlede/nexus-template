#!/usr/bin/env python3
"""
Export complete Airtable base schema to YAML.

Usage:
    python export_base_schema.py <base_id> [--output <path>]

Example:
    python export_base_schema.py appFPoOfBpUv73M5A
    python export_base_schema.py appFPoOfBpUv73M5A --output 01-memory/integrations/airtable/my-base.yaml
"""

import os
import sys
import json
import argparse
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

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
    import yaml
    import requests
except ImportError as e:
    print(f"Missing dependency: {e.name}")
    print(f"Run: pip install {e.name}")
    sys.exit(1)

API_BASE_URL = 'https://api.airtable.com/v0'


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
        raise ValueError("AIRTABLE_API_KEY not set")
    return {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }


def get_base_info(base_id, headers):
    """Get base name from bases list."""
    response = requests.get(f"{API_BASE_URL}/meta/bases", headers=headers, timeout=30)
    if response.status_code == 200:
        for base in response.json().get('bases', []):
            if base.get('id') == base_id:
                return base.get('name', 'Unknown'), base.get('permissionLevel', 'unknown')
    return 'Unknown', 'unknown'


def get_full_schema(base_id, headers):
    """Get complete schema for a base including all field details."""
    response = requests.get(
        f"{API_BASE_URL}/meta/bases/{base_id}/tables",
        headers=headers,
        timeout=60
    )

    if response.status_code != 200:
        print(f"Error fetching schema: {response.status_code}")
        print(response.text)
        return None

    data = response.json()
    tables = []

    for table in data.get('tables', []):
        table_info = {
            'id': table.get('id'),
            'name': table.get('name'),
            'description': table.get('description'),
            'primary_field_id': table.get('primaryFieldId'),
            'fields': []
        }

        for field in table.get('fields', []):
            field_info = {
                'id': field.get('id'),
                'name': field.get('name'),
                'type': field.get('type'),
                'description': field.get('description')
            }

            # Include all options for complex field types
            options = field.get('options', {})
            if options:
                # Single/Multiple Select - include choices
                if 'choices' in options:
                    field_info['choices'] = [
                        {'id': c.get('id'), 'name': c.get('name'), 'color': c.get('color')}
                        for c in options['choices']
                    ]

                # Linked records
                if 'linkedTableId' in options:
                    field_info['linked_table_id'] = options['linkedTableId']
                    field_info['prefer_single_record_link'] = options.get('prefersSingleRecordLink', False)
                    field_info['inverse_link_field_id'] = options.get('inverseLinkFieldId')

                # Lookup fields
                if 'recordLinkFieldId' in options:
                    field_info['record_link_field_id'] = options['recordLinkFieldId']
                    field_info['lookup_field_id'] = options.get('fieldIdInLinkedTable')

                # Rollup fields
                if 'referencedFieldIds' in options:
                    field_info['referenced_field_ids'] = options['referencedFieldIds']

                # Formula fields
                if 'formula' in options:
                    field_info['formula'] = options['formula']

                # Date fields
                if 'dateFormat' in options:
                    field_info['date_format'] = options['dateFormat']
                if 'timeFormat' in options:
                    field_info['time_format'] = options['timeFormat']
                if 'timeZone' in options:
                    field_info['time_zone'] = options['timeZone']

                # Number fields
                if 'precision' in options:
                    field_info['precision'] = options['precision']

                # Currency fields
                if 'symbol' in options:
                    field_info['currency_symbol'] = options['symbol']

                # Rating fields
                if 'max' in options:
                    field_info['max'] = options['max']
                if 'icon' in options:
                    field_info['icon'] = options['icon']

            table_info['fields'].append(field_info)

        # Include views if available
        if 'views' in table:
            table_info['views'] = [
                {'id': v.get('id'), 'name': v.get('name'), 'type': v.get('type')}
                for v in table.get('views', [])
            ]

        tables.append(table_info)

    return tables


def slugify(name):
    """Convert name to filesystem-safe slug."""
    import re
    # Remove special chars, replace spaces/underscores with hyphens
    slug = re.sub(r'[^\w\s-]', '', name)
    slug = re.sub(r'[\s_]+', '-', slug)
    return slug.lower().strip('-')


def main():
    parser = argparse.ArgumentParser(description='Export Airtable base schema')
    parser.add_argument('base_id', help='Airtable base ID (starts with app)')
    parser.add_argument('--output', '-o', help='Output directory path')
    parser.add_argument('--json', action='store_true', help='Output as JSON instead of YAML')
    parser.add_argument('--single-file', action='store_true', help='Export all tables to single file (default: one file per table)')
    args = parser.parse_args()

    load_env()
    headers = get_headers()

    print(f"Fetching schema for base: {args.base_id}")

    # Get base name
    base_name, permission = get_base_info(args.base_id, headers)
    print(f"Base: {base_name} ({permission})")

    # Get full schema
    tables = get_full_schema(args.base_id, headers)
    if not tables:
        print("Failed to fetch schema")
        sys.exit(1)

    print(f"Found {len(tables)} table(s)")

    # Determine output directory
    if args.output:
        output_dir = args.output
    else:
        output_dir = os.path.join(NEXUS_ROOT, '01-memory', 'integrations', 'airtable', slugify(base_name))

    os.makedirs(output_dir, exist_ok=True)
    ext = '.json' if args.json else '.yaml'

    if args.single_file:
        # Single file mode (original behavior)
        schema = {
            'base_id': args.base_id,
            'base_name': base_name,
            'permission_level': permission,
            'exported_at': datetime.now().isoformat(),
            'table_count': len(tables),
            'tables': tables
        }
        output_path = os.path.join(output_dir, f"_all-tables{ext}")
        with open(output_path, 'w', encoding='utf-8') as f:
            if args.json:
                json.dump(schema, f, indent=2, ensure_ascii=False)
            else:
                yaml.dump(schema, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        print(f"\nSchema saved to: {output_path}")
    else:
        # One file per table (default)
        # First create _index file with base info and table list
        index = {
            'base_id': args.base_id,
            'base_name': base_name,
            'permission_level': permission,
            'exported_at': datetime.now().isoformat(),
            'table_count': len(tables),
            'tables': [
                {
                    'id': t['id'],
                    'name': t['name'],
                    'file': f"{slugify(t['name'])}{ext}",
                    'field_count': len(t.get('fields', []))
                }
                for t in tables
            ]
        }
        index_path = os.path.join(output_dir, f"_index{ext}")
        with open(index_path, 'w', encoding='utf-8') as f:
            if args.json:
                json.dump(index, f, indent=2, ensure_ascii=False)
            else:
                yaml.dump(index, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        print(f"\nIndex saved to: {index_path}")

        # Now create one file per table
        for table in tables:
            table_schema = {
                'base_id': args.base_id,
                'base_name': base_name,
                'table_id': table['id'],
                'table_name': table['name'],
                'exported_at': datetime.now().isoformat(),
                'field_count': len(table.get('fields', [])),
                'fields': table.get('fields', []),
                'views': table.get('views', [])
            }
            table_path = os.path.join(output_dir, f"{slugify(table['name'])}{ext}")
            with open(table_path, 'w', encoding='utf-8') as f:
                if args.json:
                    json.dump(table_schema, f, indent=2, ensure_ascii=False)
                else:
                    yaml.dump(table_schema, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        print(f"Created {len(tables)} table files in: {output_dir}")

    # Print summary
    print("\nTables:")
    for table in tables:
        field_count = len(table.get('fields', []))
        print(f"  - {table['name']}: {field_count} fields")


if __name__ == '__main__':
    main()
