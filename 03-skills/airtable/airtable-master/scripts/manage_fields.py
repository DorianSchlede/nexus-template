#!/usr/bin/env python3
"""
Airtable Field Management

Create and update fields in Airtable tables.

Usage:
    python manage_fields.py <command> --base <BASE_ID> --table <TABLE_ID> [OPTIONS]

Commands:
    list      List all fields in a table
    create    Create a new field
    update    Update an existing field

Options:
    --base BASE        Base ID (appXXX) - required
    --table TABLE      Table ID (tblXXX) or name - required
    --token NAME       Token name (e.g., MUTAGENT -> uses AIRTABLE_API_KEY_MUTAGENT)
    --json             Output as JSON
    --verbose          Show debug info

Field Types:
    singleLineText, multilineText, email, url, phoneNumber
    number, currency, percent, duration, rating
    singleSelect, multipleSelects
    checkbox, date, dateTime
    singleCollaborator, multipleCollaborators
    multipleAttachments, multipleRecordLinks
    formula, rollup, count, lookup
    autoNumber, barcode, button, richText

Examples:
    # List fields
    python manage_fields.py list --base app1gngDx52VAgjVQ --table tblXXX --token MUTAGENT

    # Create a text field
    python manage_fields.py create --base appXXX --table tblYYY \\
        --name "Description" --type multilineText --token MUTAGENT

    # Create a select field with options
    python manage_fields.py create --base appXXX --table tblYYY \\
        --name "Status" --type singleSelect \\
        --options '{"choices": [{"name": "Todo"}, {"name": "In Progress"}, {"name": "Done"}]}' \\
        --token MUTAGENT

    # Create a number field
    python manage_fields.py create --base appXXX --table tblYYY \\
        --name "Priority" --type number --options '{"precision": 0}' \\
        --token MUTAGENT
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
    print("❌ Error: Could not find Nexus root")
    sys.exit(1)

sys.path.insert(0, NEXUS_ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import yaml
    import requests
except ImportError as e:
    print(f"❌ Missing dependency: {e.name}")
    print(f"   Run: pip install {e.name}")
    sys.exit(1)

# Import shared utilities
try:
    from airtable_utils import get_headers, load_env, make_request_with_retry
except ImportError:
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
                print(f"   ⏳ Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            return response
        return response


API_BASE_URL = 'https://api.airtable.com/v0'


# Field type info for help
FIELD_TYPES = {
    'singleLineText': {'description': 'Single line of text', 'options': None},
    'multilineText': {'description': 'Multiple lines of text', 'options': None},
    'email': {'description': 'Email address', 'options': None},
    'url': {'description': 'URL link', 'options': None},
    'phoneNumber': {'description': 'Phone number', 'options': None},
    'number': {'description': 'Number', 'options': {'precision': '0-8'}},
    'currency': {'description': 'Currency value', 'options': {'precision': '0-7', 'symbol': '$'}},
    'percent': {'description': 'Percentage', 'options': {'precision': '0-8'}},
    'duration': {'description': 'Duration', 'options': {'durationFormat': 'h:mm'}},
    'rating': {'description': 'Star rating', 'options': {'max': '1-10', 'icon': 'star'}},
    'singleSelect': {'description': 'Single choice', 'options': {'choices': '[{name: ...}]'}},
    'multipleSelects': {'description': 'Multiple choices', 'options': {'choices': '[{name: ...}]'}},
    'checkbox': {'description': 'Checkbox (true/false)', 'options': None},
    'date': {'description': 'Date only', 'options': {'dateFormat': {'name': 'local/friendly/iso'}}},
    'dateTime': {'description': 'Date and time', 'options': {'dateFormat': {...}, 'timeFormat': {...}}},
    'singleCollaborator': {'description': 'Single user', 'options': None},
    'multipleCollaborators': {'description': 'Multiple users', 'options': None},
    'multipleAttachments': {'description': 'File attachments', 'options': None},
    'multipleRecordLinks': {'description': 'Links to other table', 'options': {'linkedTableId': 'tblXXX'}},
}


def list_fields(base_id, table_id, token_name=None, verbose=False):
    """List all fields in a table by getting table schema."""
    headers = get_headers(token_name)
    url = f"{API_BASE_URL}/meta/bases/{base_id}/tables"

    if verbose:
        print(f"[INFO] Fetching table schema from {url}", file=sys.stderr)

    try:
        response = make_request_with_retry('GET', url, headers)

        if response.status_code == 200:
            data = response.json()
            tables = data.get('tables', [])

            # Find the target table
            for table in tables:
                if table.get('id') == table_id or table.get('name').lower() == table_id.lower():
                    return table.get('fields', [])

            print(f"❌ Table not found: {table_id}", file=sys.stderr)
            return None
        else:
            print(f"❌ API error: {response.status_code}", file=sys.stderr)
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}", file=sys.stderr)
        return None


def create_field(base_id, table_id, name, field_type, description=None, options=None, token_name=None, verbose=False):
    """
    Create a new field in a table.

    Args:
        base_id: Base ID (appXXX)
        table_id: Table ID (tblXXX)
        name: Field name
        field_type: Field type (e.g., singleLineText, singleSelect)
        description: Optional field description
        options: Type-specific options (e.g., choices for select)
        token_name: Optional token name
        verbose: Show debug info

    Returns:
        Created field object or None on error
    """
    headers = get_headers(token_name)
    url = f"{API_BASE_URL}/meta/bases/{base_id}/tables/{table_id}/fields"

    body = {
        "name": name,
        "type": field_type
    }

    if description:
        body["description"] = description

    if options:
        body["options"] = options

    if verbose:
        print(f"[INFO] Creating field '{name}' ({field_type}) in {table_id}", file=sys.stderr)

    try:
        response = make_request_with_retry('POST', url, headers, body)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            error = response.json().get('error', {})
            print(f"❌ Bad request: {error.get('message', 'Unknown error')}", file=sys.stderr)
            if verbose:
                print(f"   Response: {response.text}", file=sys.stderr)
            return None
        elif response.status_code == 401:
            print("❌ 401 Unauthorized - Invalid API key", file=sys.stderr)
            return None
        elif response.status_code == 403:
            print("❌ 403 Forbidden - No permission to create fields", file=sys.stderr)
            return None
        elif response.status_code == 404:
            print(f"❌ Table not found: {table_id}", file=sys.stderr)
            return None
        elif response.status_code == 422:
            error = response.json().get('error', {})
            print(f"❌ Validation error: {error.get('message', 'Unknown error')}", file=sys.stderr)
            if verbose:
                print(f"   Response: {response.text}", file=sys.stderr)
            return None
        else:
            print(f"❌ Create failed: {response.status_code}", file=sys.stderr)
            if verbose:
                print(f"   Response: {response.text[:500]}", file=sys.stderr)
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}", file=sys.stderr)
        return None


def update_field(base_id, table_id, field_id, name=None, description=None, options=None, token_name=None, verbose=False):
    """
    Update an existing field.

    Args:
        base_id: Base ID (appXXX)
        table_id: Table ID (tblXXX)
        field_id: Field ID (fldXXX)
        name: New field name (optional)
        description: New field description (optional)
        options: Updated options (optional, for select types)
        token_name: Optional token name
        verbose: Show debug info

    Returns:
        Updated field object or None on error
    """
    headers = get_headers(token_name)
    url = f"{API_BASE_URL}/meta/bases/{base_id}/tables/{table_id}/fields/{field_id}"

    body = {}
    if name:
        body["name"] = name
    if description is not None:
        body["description"] = description
    if options:
        body["options"] = options

    if not body:
        print("❌ No updates specified", file=sys.stderr)
        return None

    if verbose:
        print(f"[INFO] Updating field {field_id} in {table_id}", file=sys.stderr)

    try:
        response = make_request_with_retry('PATCH', url, headers, body)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            error = response.json().get('error', {})
            print(f"❌ Bad request: {error.get('message', 'Unknown error')}", file=sys.stderr)
            return None
        elif response.status_code == 404:
            print(f"❌ Field not found: {field_id}", file=sys.stderr)
            return None
        else:
            print(f"❌ Update failed: {response.status_code}", file=sys.stderr)
            if verbose:
                print(f"   Response: {response.text[:500]}", file=sys.stderr)
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}", file=sys.stderr)
        return None


def format_field_info(field, primary_field_id=None):
    """Format field info for display."""
    name = field.get('name', 'Untitled')
    field_id = field.get('id', 'unknown')
    field_type = field.get('type', 'unknown')
    is_primary = "⭐" if field_id == primary_field_id else ""
    description = field.get('description', '')

    lines = [f"  {is_primary} {name}"]
    lines.append(f"      ID: {field_id}")
    lines.append(f"      Type: {field_type}")

    if description:
        lines.append(f"      Description: {description}")

    # Show options for select types
    options = field.get('options', {})
    if field_type in ['singleSelect', 'multipleSelects'] and 'choices' in options:
        choices = [c.get('name') for c in options['choices'][:5]]
        if len(options['choices']) > 5:
            choices.append(f"... +{len(options['choices']) - 5} more")
        lines.append(f"      Choices: {', '.join(choices)}")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Manage Airtable fields',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # List command
    list_parser = subparsers.add_parser('list', help='List all fields in a table')
    list_parser.add_argument('--base', required=True, help='Base ID (appXXX)')
    list_parser.add_argument('--table', required=True, help='Table ID (tblXXX) or name')
    list_parser.add_argument('--token', help='Token name (e.g., MUTAGENT)')
    list_parser.add_argument('--json', action='store_true', help='Output as JSON')
    list_parser.add_argument('--verbose', '-v', action='store_true', help='Show debug info')

    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new field')
    create_parser.add_argument('--base', required=True, help='Base ID (appXXX)')
    create_parser.add_argument('--table', required=True, help='Table ID (tblXXX)')
    create_parser.add_argument('--name', required=True, help='Field name')
    create_parser.add_argument('--type', required=True, dest='field_type', help='Field type')
    create_parser.add_argument('--description', help='Field description')
    create_parser.add_argument('--options', help='JSON options for field type')
    create_parser.add_argument('--token', help='Token name (e.g., MUTAGENT)')
    create_parser.add_argument('--json', action='store_true', help='Output as JSON')
    create_parser.add_argument('--verbose', '-v', action='store_true', help='Show debug info')

    # Update command
    update_parser = subparsers.add_parser('update', help='Update an existing field')
    update_parser.add_argument('--base', required=True, help='Base ID (appXXX)')
    update_parser.add_argument('--table', required=True, help='Table ID (tblXXX)')
    update_parser.add_argument('--field', required=True, help='Field ID (fldXXX)')
    update_parser.add_argument('--name', help='New field name')
    update_parser.add_argument('--description', help='New field description')
    update_parser.add_argument('--options', help='Updated options JSON')
    update_parser.add_argument('--token', help='Token name (e.g., MUTAGENT)')
    update_parser.add_argument('--json', action='store_true', help='Output as JSON')
    update_parser.add_argument('--verbose', '-v', action='store_true', help='Show debug info')

    # Types command (help)
    types_parser = subparsers.add_parser('types', help='Show available field types')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Load environment
    load_env()

    # Show token info
    if hasattr(args, 'token') and args.token and not getattr(args, 'json', False):
        print(f"🔑 Using token: AIRTABLE_API_KEY_{args.token.upper()}")

    # Execute command
    if args.command == 'types':
        print("\n📋 Available Field Types:\n")
        for ftype, info in FIELD_TYPES.items():
            options_str = f" (options: {info['options']})" if info['options'] else ""
            print(f"  {ftype}: {info['description']}{options_str}")
        print()
        sys.exit(0)

    elif args.command == 'list':
        fields = list_fields(args.base, args.table, args.token, args.verbose)

        if fields is None:
            sys.exit(1)

        if args.json:
            print(json.dumps({'fields': fields, 'count': len(fields)}, indent=2))
        else:
            print(f"\n📊 Found {len(fields)} field(s)\n")
            for field in fields:
                print(format_field_info(field))
                print()

    elif args.command == 'create':
        # Parse options if provided
        options = None
        if args.options:
            try:
                options = json.loads(args.options)
            except json.JSONDecodeError as e:
                print(f"❌ Invalid JSON for --options: {e}")
                sys.exit(1)

        if not args.json:
            print(f"\n📝 Creating field '{args.name}' ({args.field_type})...")

        result = create_field(
            args.base,
            args.table,
            args.name,
            args.field_type,
            description=args.description,
            options=options,
            token_name=args.token,
            verbose=args.verbose
        )

        if result:
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"\n✅ Field created successfully!")
                print(f"   ID: {result.get('id')}")
                print(f"   Name: {result.get('name')}")
                print(f"   Type: {result.get('type')}")
        else:
            sys.exit(1)

    elif args.command == 'update':
        # Parse options if provided
        options = None
        if args.options:
            try:
                options = json.loads(args.options)
            except json.JSONDecodeError as e:
                print(f"❌ Invalid JSON for --options: {e}")
                sys.exit(1)

        if not args.json:
            print(f"\n📝 Updating field {args.field}...")

        result = update_field(
            args.base,
            args.table,
            args.field,
            name=args.name,
            description=args.description,
            options=options,
            token_name=args.token,
            verbose=args.verbose
        )

        if result:
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"\n✅ Field updated successfully!")
                print(f"   ID: {result.get('id')}")
                print(f"   Name: {result.get('name')}")
        else:
            sys.exit(1)


if __name__ == '__main__':
    main()
