#!/usr/bin/env python3
"""
Airtable Base Discovery

Discover and cache all accessible bases from Airtable.

Usage:
    python discover_bases.py [--refresh] [--json] [--with-schema]

Options:
    --refresh       Force re-discovery even if cache exists
    --json          Output as JSON only (no progress messages)
    --with-schema   Also fetch table schemas (slower)

Output:
    Saves to: 01-memory/integrations/airtable-bases.yaml
"""

import os
import sys
import json
import argparse
from datetime import datetime

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


# Configuration
CACHE_FILE = os.path.join(NEXUS_ROOT, '01-memory', 'integrations', 'airtable-bases.yaml')
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


def discover_bases(verbose=True):
    """Discover all accessible bases."""
    headers = get_headers()
    bases = []

    if verbose:
        print("🔍 Discovering Airtable bases...")

    try:
        response = requests.get(
            f"{API_BASE_URL}/meta/bases",
            headers=headers,
            timeout=30
        )

        if response.status_code != 200:
            if verbose:
                print(f"   ❌ API error: {response.status_code}")
            return []

        data = response.json()
        raw_bases = data.get('bases', [])

        for base in raw_bases:
            base_info = {
                'id': base.get('id'),
                'name': base.get('name', 'Unnamed'),
                'permission_level': base.get('permissionLevel', 'unknown')
            }
            bases.append(base_info)

            if verbose:
                print(f"   ✓ {base_info['name']} ({base_info['permission_level']})")

    except requests.exceptions.RequestException as e:
        if verbose:
            print(f"   ❌ Request failed: {e}")
        return []

    if verbose:
        print(f"\n📊 Found {len(bases)} base(s)")

    return bases


def get_base_schema(base_id, headers, verbose=True):
    """Get table schema for a specific base."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/meta/bases/{base_id}/tables",
            headers=headers,
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            tables = []
            for table in data.get('tables', []):
                table_info = {
                    'id': table.get('id'),
                    'name': table.get('name'),
                    'primary_field_id': table.get('primaryFieldId'),
                    'fields': []
                }

                for field in table.get('fields', []):
                    field_info = {
                        'id': field.get('id'),
                        'name': field.get('name'),
                        'type': field.get('type')
                    }
                    # Add options for select fields
                    if field.get('options'):
                        if 'choices' in field['options']:
                            field_info['choices'] = [c.get('name') for c in field['options']['choices']]
                    table_info['fields'].append(field_info)

                tables.append(table_info)

            return tables
        else:
            return None

    except requests.exceptions.RequestException:
        return None


def save_cache(bases, with_schema=False):
    """Save discovered bases to cache file."""
    # Ensure directory exists
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)

    cache_data = {
        'discovered_at': datetime.now().isoformat(),
        'total_bases': len(bases),
        'includes_schema': with_schema,
        'bases': bases
    }

    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(cache_data, f, default_flow_style=False, allow_unicode=True)

    return CACHE_FILE


def load_cache():
    """Load cached bases if available."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return None


def main():
    parser = argparse.ArgumentParser(description='Discover Airtable bases')
    parser.add_argument('--refresh', action='store_true', help='Force re-discovery')
    parser.add_argument('--json', action='store_true', help='Output as JSON only')
    parser.add_argument('--with-schema', action='store_true', help='Include table schemas')
    args = parser.parse_args()

    # Load environment
    load_env()

    # Check cache
    if not args.refresh:
        cache = load_cache()
        if cache:
            # Check if we need schema but cache doesn't have it
            if args.with_schema and not cache.get('includes_schema'):
                pass  # Need to refresh
            else:
                if args.json:
                    print(json.dumps(cache, indent=2))
                else:
                    print(f"📦 Using cached data from {cache['discovered_at']}")
                    print(f"   Total bases: {cache['total_bases']}")
                    print(f"   Cache: {CACHE_FILE}")
                    print(f"\n   Use --refresh to re-discover")
                sys.exit(0)

    # Discover bases
    verbose = not args.json
    bases = discover_bases(verbose=verbose)

    if not bases:
        if not args.json:
            print("❌ No bases found or discovery failed")
            print("   Add bases to your PAT at: https://airtable.com/create/tokens")
        sys.exit(1)

    # Optionally fetch schemas
    if args.with_schema:
        headers = get_headers()
        if verbose:
            print("\n📋 Fetching table schemas...")
        for base in bases:
            tables = get_base_schema(base['id'], headers, verbose)
            if tables:
                base['tables'] = tables
                if verbose:
                    print(f"   ✓ {base['name']}: {len(tables)} table(s)")

    # Save cache
    cache_path = save_cache(bases, with_schema=args.with_schema)

    if args.json:
        result = {
            'discovered_at': datetime.now().isoformat(),
            'total_bases': len(bases),
            'includes_schema': args.with_schema,
            'bases': bases
        }
        print(json.dumps(result, indent=2))
    else:
        print(f"\n✅ Saved to: {cache_path}")


if __name__ == '__main__':
    main()
