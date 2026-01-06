#!/usr/bin/env python3
"""
Airtable Record Query

Query records from an Airtable table with filtering and pagination.

Usage:
    python query_records.py --base <BASE_ID_OR_NAME> --table <TABLE_ID_OR_NAME> [OPTIONS]

Options:
    --base BASE        Base ID (appXXX) or name
    --table TABLE      Table ID (tblXXX) or name
    --filter FORMULA   Airtable formula filter
    --fields FIELDS    Comma-separated field names
    --view VIEW        View ID or name
    --sort FIELD       Sort by field (prefix with - for desc)
    --limit N          Max records to return
    --token NAME       Token name (e.g., MUTAGENT -> uses AIRTABLE_API_KEY_MUTAGENT)
    --json             Output as JSON
    --verbose          Show debug info

Examples:
    python query_records.py --base "My CRM" --table "Contacts"
    python query_records.py --base appXXX --table tblYYY --filter "{Status}='Active'" --token MUTAGENT
    python query_records.py --base "Tasks" --table "Tasks" --sort "-Due Date" --limit 10
"""

import os
import sys
import json
import argparse
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
    print("❌ Error: Could not find Nexus root")
    sys.exit(1)

sys.path.insert(0, NEXUS_ROOT)

try:
    import yaml
    import requests
except ImportError as e:
    print(f"❌ Missing dependency: {e.name}")
    print(f"   Run: pip install {e.name}")
    sys.exit(1)


API_BASE_URL = 'https://api.airtable.com/v0'
CACHE_FILE = os.path.join(NEXUS_ROOT, '01-memory', 'integrations', 'airtable-bases.yaml')


# Import shared utilities
try:
    from airtable_utils import get_headers, load_env, resolve_base_id
except ImportError:
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

    def get_headers(token_name=None):
        """Get API headers."""
        if token_name:
            key_name = f"AIRTABLE_API_KEY_{token_name.upper()}"
        else:
            key_name = "AIRTABLE_API_KEY"
        api_key = os.environ.get(key_name)
        if not api_key:
            raise ValueError(f"{key_name} not set")
        return {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

# Global token name
_token_name = None


def load_base_cache():
    """Load cached base info."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return None


def _resolve_base_id(base_ref, token_name=None, verbose=False):
    """Resolve base name to ID."""
    # If already an ID
    if base_ref.startswith('app'):
        return base_ref

    # Try to find in cache
    cache = load_base_cache()
    if cache:
        for base in cache.get('bases', []):
            if base.get('name', '').lower() == base_ref.lower():
                if verbose:
                    print(f"   Resolved base '{base_ref}' → {base['id']}")
                return base['id']

    # Try API lookup
    try:
        headers = get_headers(token_name)
        response = requests.get(f"{API_BASE_URL}/meta/bases", headers=headers, timeout=10)
        if response.status_code == 200:
            for base in response.json().get('bases', []):
                if base.get('name', '').lower() == base_ref.lower():
                    if verbose:
                        print(f"   Resolved base '{base_ref}' → {base['id']}")
                    return base['id']
    except:
        pass

    print(f"❌ Could not find base: {base_ref}")
    sys.exit(1)


def query_records(base_id, table_ref, filter_formula=None, fields=None, view=None,
                  sort_field=None, limit=None, verbose=False, token_name=None):
    """Query records from a table."""
    headers = get_headers(token_name)
    records = []

    # URL encode table name if it contains spaces
    table_encoded = urllib.parse.quote(table_ref, safe='')
    url = f"{API_BASE_URL}/{base_id}/{table_encoded}"

    offset = None
    total_fetched = 0

    while True:
        params = {'pageSize': min(100, limit - total_fetched if limit else 100)}

        if offset:
            params['offset'] = offset

        if filter_formula:
            params['filterByFormula'] = filter_formula

        if fields:
            for field in fields:
                params.setdefault('fields[]', []).append(field)

        if view:
            params['view'] = view

        if sort_field:
            direction = 'desc' if sort_field.startswith('-') else 'asc'
            field_name = sort_field.lstrip('-')
            params['sort[0][field]'] = field_name
            params['sort[0][direction]'] = direction

        if verbose:
            print(f"   Fetching from {url}...")

        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)

            if response.status_code == 404:
                print(f"❌ Table not found: {table_ref}")
                print("   Check table name or use table ID (tblXXX)")
                sys.exit(1)

            if response.status_code == 422:
                error = response.json().get('error', {})
                print(f"❌ Invalid request: {error.get('message', 'Unknown error')}")
                sys.exit(1)

            if response.status_code != 200:
                print(f"❌ API error: {response.status_code}")
                if verbose:
                    print(f"   Response: {response.text[:500]}")
                sys.exit(1)

            data = response.json()
            batch = data.get('records', [])
            records.extend(batch)
            total_fetched += len(batch)

            if verbose:
                print(f"   Fetched {len(batch)} records (total: {total_fetched})")

            # Check if we've hit the limit
            if limit and total_fetched >= limit:
                records = records[:limit]
                break

            # Check for more pages
            offset = data.get('offset')
            if not offset:
                break

        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            sys.exit(1)

    return records


def format_record(record, fields_to_show=None):
    """Format a record for display."""
    rec_id = record.get('id', 'unknown')
    fields = record.get('fields', {})

    if fields_to_show:
        fields = {k: v for k, v in fields.items() if k in fields_to_show}

    lines = [f"Record: {rec_id}"]
    for key, value in fields.items():
        if isinstance(value, list):
            value = ', '.join(str(v) for v in value)
        elif isinstance(value, dict):
            value = json.dumps(value)
        lines.append(f"  {key}: {value}")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Query Airtable records')
    parser.add_argument('--base', required=True, help='Base ID or name')
    parser.add_argument('--table', required=True, help='Table ID or name')
    parser.add_argument('--filter', dest='filter_formula', help='Airtable formula filter')
    parser.add_argument('--fields', help='Comma-separated field names')
    parser.add_argument('--view', help='View ID or name')
    parser.add_argument('--sort', dest='sort_field', help='Sort field (prefix - for desc)')
    parser.add_argument('--limit', type=int, help='Max records to return')
    parser.add_argument('--token', help='Token name (e.g., MUTAGENT -> uses AIRTABLE_API_KEY_MUTAGENT)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show debug info')
    args = parser.parse_args()

    # Load environment
    load_env()

    # Show token info
    if args.token and not args.json:
        print(f"🔑 Using token: AIRTABLE_API_KEY_{args.token.upper()}")

    # Resolve base ID
    base_id = _resolve_base_id(args.base, args.token, args.verbose)

    # Parse fields
    fields = args.fields.split(',') if args.fields else None

    # Query records
    if not args.json:
        print(f"\n🔍 Querying {args.table} in {args.base}...")
        if args.filter_formula:
            print(f"   Filter: {args.filter_formula}")

    records = query_records(
        base_id=base_id,
        table_ref=args.table,
        filter_formula=args.filter_formula,
        fields=fields,
        view=args.view,
        sort_field=args.sort_field,
        limit=args.limit,
        verbose=args.verbose,
        token_name=args.token
    )

    if args.json:
        print(json.dumps({'records': records, 'count': len(records)}, indent=2))
    else:
        print(f"\n📊 Found {len(records)} record(s)\n")

        if records:
            # Show first few records
            show_count = min(5, len(records))
            for record in records[:show_count]:
                print(format_record(record, fields))
                print()

            if len(records) > show_count:
                print(f"... and {len(records) - show_count} more")
                print("Use --json for full output")


if __name__ == '__main__':
    main()
