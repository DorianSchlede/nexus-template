#!/usr/bin/env python3
"""
Airtable Table Management

Create, update, and list tables in Airtable bases.

Usage:
    python manage_tables.py <command> --base <BASE_ID> [OPTIONS]

Commands:
    list      List all tables in a base
    create    Create a new table
    update    Update an existing table

Options:
    --base BASE        Base ID (appXXX) - required
    --token NAME       Token name (e.g., MUTAGENT -> uses AIRTABLE_API_KEY_MUTAGENT)
    --json             Output as JSON
    --verbose          Show debug info

Examples:
    # List tables
    python manage_tables.py list --base app1gngDx52VAgjVQ --token MUTAGENT

    # Create a simple table
    python manage_tables.py create --base app1gngDx52VAgjVQ --name "Projects" \\
        --token MUTAGENT

    # Create table with fields
    python manage_tables.py create --base app1gngDx52VAgjVQ --name "Tasks" \\
        --fields '[{"name": "Name", "type": "singleLineText"}, {"name": "Status", "type": "singleSelect", "options": {"choices": [{"name": "Todo"}, {"name": "Done"}]}}]' \\
        --token MUTAGENT

    # Update table name
    python manage_tables.py update --base app1gngDx52VAgjVQ --table tblXXX \\
        --name "New Name" --token MUTAGENT
"""

import os
import sys
import json
import argparse
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

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
    print("[ERROR] Error: Could not find Nexus root")
    sys.exit(1)

sys.path.insert(0, NEXUS_ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import yaml
    import requests
except ImportError as e:
    print(f"[ERROR] Missing dependency: {e.name}")
    print(f"   Run: pip install {e.name}")
    sys.exit(1)

# Import shared utilities
try:
    from airtable_utils import get_headers, load_env, make_request_with_retry, update_context_file, get_cache_file_path
except ImportError:
    # Fallback implementations
    def load_env():
        env_path = os.path.join(NEXUS_ROOT, '.env')
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip().strip('"\'')

    def get_headers(token_name=None):
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

    def make_request_with_retry(method, url, headers, json_data=None, max_retries=3):
        import time
        for attempt in range(max_retries):
            response = requests.request(method, url, headers=headers, json=json_data, timeout=30)
            if response.status_code == 429:
                wait = min(30, 2 ** attempt)
                print(f"   [WAIT] Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            return response
        return response


API_BASE_URL = 'https://api.airtable.com/v0'


def list_tables(base_id, token_name=None, verbose=False):
    """List all tables in a base."""
    headers = get_headers(token_name)
    url = f"{API_BASE_URL}/meta/bases/{base_id}/tables"

    if verbose:
        print(f"[INFO] Fetching tables from {url}", file=sys.stderr)

    try:
        response = make_request_with_retry('GET', url, headers)

        if response.status_code == 200:
            data = response.json()
            return data.get('tables', [])
        elif response.status_code == 401:
            print("[ERROR] 401 Unauthorized - Invalid API key", file=sys.stderr)
            return None
        elif response.status_code == 403:
            print("[ERROR] 403 Forbidden - No access to this base", file=sys.stderr)
            return None
        elif response.status_code == 404:
            print(f"[ERROR] 404 Not Found - Base {base_id} not found", file=sys.stderr)
            return None
        else:
            print(f"[ERROR] API error: {response.status_code}", file=sys.stderr)
            if verbose:
                print(f"   Response: {response.text[:500]}", file=sys.stderr)
            return None

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed: {e}", file=sys.stderr)
        return None


def create_table(base_id, name, description=None, fields=None, token_name=None, verbose=False):
    """
    Create a new table in a base.

    Args:
        base_id: Base ID (appXXX)
        name: Table name
        description: Optional table description
        fields: List of field definitions
        token_name: Optional token name
        verbose: Show debug info

    Returns:
        Created table object or None on error
    """
    headers = get_headers(token_name)
    url = f"{API_BASE_URL}/meta/bases/{base_id}/tables"

    # Build request body
    body = {
        "name": name,
        "fields": fields or [
            {"name": "Name", "type": "singleLineText"}  # Default primary field
        ]
    }

    if description:
        body["description"] = description

    if verbose:
        print(f"[INFO] Creating table '{name}' in {base_id}", file=sys.stderr)
        print(f"[INFO] Fields: {len(body['fields'])}", file=sys.stderr)

    try:
        response = make_request_with_retry('POST', url, headers, body)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            error = response.json().get('error', {})
            print(f"[ERROR] Bad request: {error.get('message', 'Unknown error')}", file=sys.stderr)
            if verbose:
                print(f"   Response: {response.text}", file=sys.stderr)
            return None
        elif response.status_code == 401:
            print("[ERROR] 401 Unauthorized - Invalid API key", file=sys.stderr)
            return None
        elif response.status_code == 403:
            print("[ERROR] 403 Forbidden - No permission to create tables", file=sys.stderr)
            return None
        elif response.status_code == 422:
            error = response.json().get('error', {})
            print(f"[ERROR] Validation error: {error.get('message', 'Unknown error')}", file=sys.stderr)
            return None
        else:
            print(f"[ERROR] Create failed: {response.status_code}", file=sys.stderr)
            if verbose:
                print(f"   Response: {response.text[:500]}", file=sys.stderr)
            return None

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed: {e}", file=sys.stderr)
        return None


def update_table(base_id, table_id, name=None, description=None, token_name=None, verbose=False):
    """
    Update an existing table.

    Args:
        base_id: Base ID (appXXX)
        table_id: Table ID (tblXXX)
        name: New table name (optional)
        description: New table description (optional)
        token_name: Optional token name
        verbose: Show debug info

    Returns:
        Updated table object or None on error
    """
    headers = get_headers(token_name)
    url = f"{API_BASE_URL}/meta/bases/{base_id}/tables/{table_id}"

    body = {}
    if name:
        body["name"] = name
    if description is not None:
        body["description"] = description

    if not body:
        print("[ERROR] No updates specified (--name or --description required)", file=sys.stderr)
        return None

    if verbose:
        print(f"[INFO] Updating table {table_id} in {base_id}", file=sys.stderr)

    try:
        response = make_request_with_retry('PATCH', url, headers, body)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            error = response.json().get('error', {})
            print(f"[ERROR] Bad request: {error.get('message', 'Unknown error')}", file=sys.stderr)
            return None
        elif response.status_code == 404:
            print(f"[ERROR] Table not found: {table_id}", file=sys.stderr)
            return None
        else:
            print(f"[ERROR] Update failed: {response.status_code}", file=sys.stderr)
            if verbose:
                print(f"   Response: {response.text[:500]}", file=sys.stderr)
            return None

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed: {e}", file=sys.stderr)
        return None


def format_table_info(table):
    """Format table info for display."""
    name = table.get('name', 'Untitled')
    table_id = table.get('id', 'unknown')
    fields = table.get('fields', [])
    primary_field = table.get('primaryFieldId', '')

    lines = [f"[LIST] {name}"]
    lines.append(f"   ID: {table_id}")
    lines.append(f"   Fields: {len(fields)}")

    if fields:
        lines.append("   Schema:")
        for field in fields[:10]:  # Show first 10 fields
            field_name = field.get('name', 'Untitled')
            field_type = field.get('type', 'unknown')
            is_primary = "[*]" if field.get('id') == primary_field else ""
            lines.append(f"     - {field_name} ({field_type}) {is_primary}")
        if len(fields) > 10:
            lines.append(f"     ... and {len(fields) - 10} more")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Manage Airtable tables',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # List command
    list_parser = subparsers.add_parser('list', help='List all tables in a base')
    list_parser.add_argument('--base', required=True, help='Base ID (appXXX)')
    list_parser.add_argument('--token', help='Token name (e.g., MUTAGENT)')
    list_parser.add_argument('--json', action='store_true', help='Output as JSON')
    list_parser.add_argument('--verbose', '-v', action='store_true', help='Show debug info')

    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new table')
    create_parser.add_argument('--base', required=True, help='Base ID (appXXX)')
    create_parser.add_argument('--name', required=True, help='Table name')
    create_parser.add_argument('--description', help='Table description')
    create_parser.add_argument('--fields', help='JSON array of field definitions')
    create_parser.add_argument('--token', help='Token name (e.g., MUTAGENT)')
    create_parser.add_argument('--json', action='store_true', help='Output as JSON')
    create_parser.add_argument('--verbose', '-v', action='store_true', help='Show debug info')

    # Update command
    update_parser = subparsers.add_parser('update', help='Update an existing table')
    update_parser.add_argument('--base', required=True, help='Base ID (appXXX)')
    update_parser.add_argument('--table', required=True, help='Table ID (tblXXX)')
    update_parser.add_argument('--name', help='New table name')
    update_parser.add_argument('--description', help='New table description')
    update_parser.add_argument('--token', help='Token name (e.g., MUTAGENT)')
    update_parser.add_argument('--json', action='store_true', help='Output as JSON')
    update_parser.add_argument('--verbose', '-v', action='store_true', help='Show debug info')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Load environment
    load_env()

    # Show token info
    if hasattr(args, 'token') and args.token and not args.json:
        print(f"[KEY] Using token: AIRTABLE_API_KEY_{args.token.upper()}")

    # Execute command
    if args.command == 'list':
        tables = list_tables(args.base, args.token, args.verbose)

        if tables is None:
            sys.exit(1)

        if args.json:
            print(json.dumps({'tables': tables, 'count': len(tables)}, indent=2))
        else:
            print(f"\n[STATS] Found {len(tables)} table(s) in {args.base}\n")
            for table in tables:
                print(format_table_info(table))
                print()

    elif args.command == 'create':
        # Parse fields if provided
        fields = None
        if args.fields:
            try:
                fields = json.loads(args.fields)
            except json.JSONDecodeError as e:
                print(f"[ERROR] Invalid JSON for --fields: {e}")
                sys.exit(1)

        if not args.json:
            print(f"\n[>] Creating table '{args.name}' in {args.base}...")

        result = create_table(
            args.base,
            args.name,
            description=args.description,
            fields=fields,
            token_name=args.token,
            verbose=args.verbose
        )

        if result:
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"\n[OK] Table created successfully!")
                print(f"   ID: {result.get('id')}")
                print(f"   Name: {result.get('name')}")
                print(f"   Fields: {len(result.get('fields', []))}")
        else:
            sys.exit(1)

    elif args.command == 'update':
        if not args.json:
            print(f"\n[>] Updating table {args.table} in {args.base}...")

        result = update_table(
            args.base,
            args.table,
            name=args.name,
            description=args.description,
            token_name=args.token,
            verbose=args.verbose
        )

        if result:
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"\n[OK] Table updated successfully!")
                print(f"   ID: {result.get('id')}")
                print(f"   Name: {result.get('name')}")
        else:
            sys.exit(1)


if __name__ == '__main__':
    main()
