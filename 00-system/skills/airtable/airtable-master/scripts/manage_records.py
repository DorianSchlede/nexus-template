#!/usr/bin/env python3
"""
Airtable Record Management

Create, update, and delete records in Airtable.

Usage:
    python manage_records.py <action> --base <BASE> --table <TABLE> [OPTIONS]

Actions:
    create    Create new record(s)
    update    Update existing record(s)
    delete    Delete record(s)

Options:
    --base BASE        Base ID (appXXX) or name
    --table TABLE      Table ID (tblXXX) or name
    --record ID        Record ID (for update/delete)
    --data JSON        JSON data for fields
    --file FILE        JSON file with record(s) data
    --typecast         Enable automatic type conversion
    --json             Output as JSON
    --verbose          Show debug info

Examples:
    # Create a record
    python manage_records.py create --base "Tasks" --table "Tasks" \\
        --data '{"Name": "New Task", "Status": "Todo"}'

    # Update a record
    python manage_records.py update --base "Tasks" --table "Tasks" \\
        --record recXXX --data '{"Status": "Done"}'

    # Delete a record
    python manage_records.py delete --base "Tasks" --table "Tasks" \\
        --record recXXX

    # Batch create from file
    python manage_records.py create --base "Tasks" --table "Tasks" \\
        --file records.json
"""

import os
import sys
import json
import argparse
import urllib.parse
import time

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


def load_base_cache():
    """Load cached base info."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return None


def resolve_base_id(base_ref, verbose=False):
    """Resolve base name to ID."""
    if base_ref.startswith('app'):
        return base_ref

    cache = load_base_cache()
    if cache:
        for base in cache.get('bases', []):
            if base.get('name', '').lower() == base_ref.lower():
                if verbose:
                    print(f"   Resolved base '{base_ref}' → {base['id']}")
                return base['id']

    try:
        headers = get_headers()
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


def make_request_with_retry(method, url, headers, json_data=None, max_retries=3):
    """Make request with exponential backoff for rate limits."""
    for attempt in range(max_retries):
        response = requests.request(method, url, headers=headers, json=json_data, timeout=30)

        if response.status_code == 429:
            # Rate limited - wait and retry
            wait = min(30, 2 ** attempt)
            print(f"   ⏳ Rate limited, waiting {wait}s...")
            time.sleep(wait)
            continue

        return response

    return response  # Return last response even if still rate limited


def create_records(base_id, table_ref, records, typecast=False, verbose=False):
    """Create new records."""
    headers = get_headers()
    table_encoded = urllib.parse.quote(table_ref, safe='')
    url = f"{API_BASE_URL}/{base_id}/{table_encoded}"

    created = []

    # Process in batches of 10
    for i in range(0, len(records), 10):
        batch = records[i:i+10]

        body = {
            'records': [{'fields': r} for r in batch]
        }
        if typecast:
            body['typecast'] = True

        if verbose:
            print(f"   Creating batch {i//10 + 1} ({len(batch)} records)...")

        response = make_request_with_retry('POST', url, headers, body)

        if response.status_code == 200:
            created_records = response.json().get('records', [])
            created.extend(created_records)
            if verbose:
                for rec in created_records:
                    print(f"      ✓ Created {rec['id']}")
        else:
            error = response.json().get('error', {})
            print(f"   ❌ Create failed: {error.get('message', response.status_code)}")
            if verbose:
                print(f"      Response: {response.text[:500]}")

    return created


def update_records(base_id, table_ref, updates, typecast=False, replace=False, verbose=False):
    """Update existing records."""
    headers = get_headers()
    table_encoded = urllib.parse.quote(table_ref, safe='')
    url = f"{API_BASE_URL}/{base_id}/{table_encoded}"

    updated = []
    method = 'PUT' if replace else 'PATCH'

    # Process in batches of 10
    for i in range(0, len(updates), 10):
        batch = updates[i:i+10]

        body = {
            'records': batch
        }
        if typecast:
            body['typecast'] = True

        if verbose:
            print(f"   Updating batch {i//10 + 1} ({len(batch)} records)...")

        response = make_request_with_retry(method, url, headers, body)

        if response.status_code == 200:
            updated_records = response.json().get('records', [])
            updated.extend(updated_records)
            if verbose:
                for rec in updated_records:
                    print(f"      ✓ Updated {rec['id']}")
        else:
            error = response.json().get('error', {})
            print(f"   ❌ Update failed: {error.get('message', response.status_code)}")
            if verbose:
                print(f"      Response: {response.text[:500]}")

    return updated


def delete_records(base_id, table_ref, record_ids, verbose=False):
    """Delete records."""
    headers = get_headers()
    table_encoded = urllib.parse.quote(table_ref, safe='')
    url = f"{API_BASE_URL}/{base_id}/{table_encoded}"

    deleted = []

    # Process in batches of 10
    for i in range(0, len(record_ids), 10):
        batch = record_ids[i:i+10]

        # Build query string
        params = '&'.join([f'records[]={rid}' for rid in batch])
        delete_url = f"{url}?{params}"

        if verbose:
            print(f"   Deleting batch {i//10 + 1} ({len(batch)} records)...")

        response = make_request_with_retry('DELETE', delete_url, headers)

        if response.status_code == 200:
            deleted_records = response.json().get('records', [])
            deleted.extend(deleted_records)
            if verbose:
                for rec in deleted_records:
                    print(f"      ✓ Deleted {rec['id']}")
        else:
            error = response.json().get('error', {})
            print(f"   ❌ Delete failed: {error.get('message', response.status_code)}")
            if verbose:
                print(f"      Response: {response.text[:500]}")

    return deleted


def main():
    parser = argparse.ArgumentParser(description='Manage Airtable records')
    parser.add_argument('action', choices=['create', 'update', 'delete'], help='Action to perform')
    parser.add_argument('--base', required=True, help='Base ID or name')
    parser.add_argument('--table', required=True, help='Table ID or name')
    parser.add_argument('--record', help='Record ID (for update/delete single)')
    parser.add_argument('--data', help='JSON data for fields')
    parser.add_argument('--file', help='JSON file with record(s) data')
    parser.add_argument('--typecast', action='store_true', help='Enable type conversion')
    parser.add_argument('--replace', action='store_true', help='Replace mode for update (PUT vs PATCH)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show debug info')
    args = parser.parse_args()

    # Load environment
    load_env()

    # Resolve base ID
    base_id = resolve_base_id(args.base, args.verbose)

    # Parse data
    records_data = None
    if args.data:
        try:
            records_data = json.loads(args.data)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in --data: {e}")
            sys.exit(1)
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                records_data = json.load(f)
        except Exception as e:
            print(f"❌ Could not read file: {e}")
            sys.exit(1)

    # Execute action
    result = None

    if args.action == 'create':
        if not records_data:
            print("❌ --data or --file required for create")
            sys.exit(1)

        # Normalize to list
        if isinstance(records_data, dict):
            records_data = [records_data]

        if not args.json:
            print(f"\n📝 Creating {len(records_data)} record(s) in {args.table}...")

        result = create_records(base_id, args.table, records_data,
                                typecast=args.typecast, verbose=args.verbose)

    elif args.action == 'update':
        if not args.record and not args.file:
            print("❌ --record or --file required for update")
            sys.exit(1)

        if args.record:
            if not args.data:
                print("❌ --data required when using --record")
                sys.exit(1)
            updates = [{'id': args.record, 'fields': records_data}]
        else:
            # File should contain records with id and fields
            if isinstance(records_data, dict):
                records_data = [records_data]
            updates = records_data

        if not args.json:
            print(f"\n📝 Updating {len(updates)} record(s) in {args.table}...")

        result = update_records(base_id, args.table, updates,
                                typecast=args.typecast, replace=args.replace, verbose=args.verbose)

    elif args.action == 'delete':
        if not args.record and not args.file:
            print("❌ --record or --file required for delete")
            sys.exit(1)

        if args.record:
            record_ids = [args.record]
        else:
            # File should contain list of record IDs or records with id
            if isinstance(records_data, list):
                record_ids = [r['id'] if isinstance(r, dict) else r for r in records_data]
            else:
                record_ids = [records_data['id']] if isinstance(records_data, dict) else [records_data]

        if not args.json:
            print(f"\n🗑️  Deleting {len(record_ids)} record(s) from {args.table}...")

        result = delete_records(base_id, args.table, record_ids, verbose=args.verbose)

    # Output result
    if args.json:
        print(json.dumps({'action': args.action, 'records': result, 'count': len(result)}, indent=2))
    else:
        print(f"\n✅ {args.action.title()}d {len(result)} record(s)")


if __name__ == '__main__':
    main()
