#!/usr/bin/env python3
"""
Sync Skills from Notion to Airtable

Queries the Notion Skills database and imports skills to Airtable.
Downloads skill files from Notion and uploads them as JSON bundles.

Usage:
    python sync_notion_to_airtable.py --base <BASE_ID> --table <TABLE_ID> --token MUTAGENT

Examples:
    # Sync all Notion skills to Airtable
    python sync_notion_to_airtable.py --base app1gngDx52VAgjVQ --table tblsQL8n9EfMAFIyD --token MUTAGENT

    # Dry run - show what would be synced
    python sync_notion_to_airtable.py --base app1gngDx52VAgjVQ --table tblsQL8n9EfMAFIyD --token MUTAGENT --dry-run

    # Sync specific skill
    python sync_notion_to_airtable.py --base app1gngDx52VAgjVQ --table tblsQL8n9EfMAFIyD --token MUTAGENT --skill "fathom"
"""

import os
import sys
import json
import base64
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
import time

# Fix Windows encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass


def find_nexus_root():
    current = os.path.dirname(os.path.abspath(__file__))
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, 'CLAUDE.md')):
            return current
        current = os.path.dirname(current)
    return None


NEXUS_ROOT = find_nexus_root()
if not NEXUS_ROOT:
    print('Error: Could not find Nexus root')
    sys.exit(1)

sys.path.insert(0, NEXUS_ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import requests
except ImportError:
    print('Missing dependency: requests')
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
                        os.environ[key.strip()] = value.strip().strip('"').strip("'")

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
        for attempt in range(max_retries):
            response = requests.request(method, url, headers=headers, json=json_data, timeout=30)
            if response.status_code == 429:
                wait = min(30, 2 ** attempt)
                print(f"   Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            return response
        return response


API_BASE_URL = 'https://api.airtable.com/v0'
NOTION_SCRIPTS = Path(NEXUS_ROOT) / '00-system' / 'skills' / 'notion' / 'notion-master' / 'scripts'


def query_notion_skills(skill_name=None):
    """Query Notion Skills database."""
    script = NOTION_SCRIPTS / 'search_skill_database.py'

    cmd = ['python', str(script), '--skills', '--json']
    if skill_name:
        cmd.extend(['--name', skill_name])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        # Filter out INFO lines
        output_lines = [l for l in result.stdout.split('\n') if not l.startswith('[INFO]')]
        json_output = '\n'.join(output_lines)
        return json.loads(json_output)
    except subprocess.TimeoutExpired:
        print("Timeout querying Notion")
        return None
    except json.JSONDecodeError as e:
        print(f"Failed to parse Notion response: {e}")
        return None
    except Exception as e:
        print(f"Error querying Notion: {e}")
        return None


def download_notion_skill_file(page_id, skill_name):
    """Download skill file from Notion page.

    Returns the skill file content as dict, or None on error.
    """
    # Get the page to find file attachments
    notion_api_key = os.environ.get('NOTION_API_KEY')
    if not notion_api_key:
        return None

    headers = {
        'Authorization': f'Bearer {notion_api_key}',
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    }

    # Get page properties
    url = f'https://api.notion.com/v1/pages/{page_id}'
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code != 200:
            return None

        page = resp.json()
        props = page.get('properties', {})

        # Find Skill file property
        skill_prop = props.get('Skill', {})
        files = skill_prop.get('files', [])

        if not files:
            return None

        # Get first file
        file_info = files[0]
        file_url = None

        if file_info.get('type') == 'file':
            file_url = file_info.get('file', {}).get('url')
        elif file_info.get('type') == 'external':
            file_url = file_info.get('external', {}).get('url')

        if not file_url:
            return None

        # Download file content
        file_resp = requests.get(file_url, timeout=60)
        if file_resp.status_code != 200:
            return None

        # Try to parse as JSON
        try:
            return file_resp.json()
        except:
            # Return raw text if not JSON
            return {'raw_content': file_resp.text}

    except Exception as e:
        print(f"   Error downloading file: {e}")
        return None


def get_existing_airtable_skills(base_id, table_id, token_name=None):
    """Get list of skill names already in Airtable."""
    headers = get_headers(token_name)
    url = f'{API_BASE_URL}/{base_id}/{table_id}'

    skills = set()
    offset = None

    while True:
        import urllib.parse
        params = {'pageSize': 100, 'fields[]': 'Name'}
        if offset:
            params['offset'] = offset

        full_url = f"{url}?{urllib.parse.urlencode(params)}"
        response = make_request_with_retry('GET', full_url, headers)

        if response.status_code != 200:
            return skills

        data = response.json()
        for rec in data.get('records', []):
            name = rec.get('fields', {}).get('Name', '')
            if name:
                skills.add(name)

        offset = data.get('offset')
        if not offset:
            break

    return skills


def create_skill_bundle_from_notion(skill_data, skill_file_content=None):
    """Create a skill bundle from Notion skill data.

    Args:
        skill_data: Dict with Notion skill properties
        skill_file_content: Optional downloaded skill file content

    Returns:
        Dict with bundle format
    """
    skill_name = skill_data.get('skill_name', 'unknown')

    # If we have a skill file, use it as the bundle
    if skill_file_content and isinstance(skill_file_content, dict):
        if 'raw_content' in skill_file_content:
            # Non-JSON file - encode as base64
            content = skill_file_content['raw_content']
            files = {
                'SKILL.skill': base64.b64encode(content.encode()).decode()
            }
        else:
            # JSON skill file - encode the whole thing
            content = json.dumps(skill_file_content, indent=2)
            files = {
                'SKILL.skill.json': base64.b64encode(content.encode()).decode()
            }
    else:
        # No file - create minimal bundle with metadata
        skill_md = f"""---
name: {skill_name}
description: {skill_data.get('description', '')}
version: {skill_data.get('version', '1.0')}
team: {skill_data.get('team', 'General')}
---

# {skill_name}

## Purpose

{skill_data.get('purpose', skill_data.get('description', 'No description available.'))}

## Source

Imported from Notion on {datetime.now().strftime('%Y-%m-%d')}
"""
        files = {
            'SKILL.md': base64.b64encode(skill_md.encode()).decode()
        }

    return {
        'skill_name': skill_name,
        'version': skill_data.get('version', '1.0'),
        'bundle_format': 'nexus-skill-bundle-v1',
        'created': datetime.now().isoformat(),
        'source': 'notion',
        'notion_page_id': skill_data.get('id', ''),
        'files': files,
        'partial': False
    }


MAX_CONTENT_SIZE = 90000  # Airtable field limit


def upload_to_airtable(base_id, table_id, skill_data, bundle, token_name=None):
    """Upload a skill to Airtable.

    Returns (success, record_id or error message)
    """
    headers = get_headers(token_name)
    url = f'{API_BASE_URL}/{base_id}/{table_id}'

    # Check content size and create partial bundle if too large
    content_json = json.dumps(bundle)
    if len(content_json) > MAX_CONTENT_SIZE:
        # Create partial bundle with just metadata
        partial_bundle = {
            'skill_name': bundle.get('skill_name'),
            'version': bundle.get('version'),
            'bundle_format': bundle.get('bundle_format'),
            'created': bundle.get('created'),
            'source': bundle.get('source'),
            'notion_page_id': bundle.get('notion_page_id'),
            'files': {},
            'partial': True,
            'original_size': len(content_json)
        }
        content_json = json.dumps(partial_bundle)

    # Build fields
    fields = {
        'Name': skill_data.get('skill_name', 'unknown'),
        'Version': skill_data.get('version', '1.0'),
        'Description': skill_data.get('description', '')[:500],  # Truncate if needed
        'Purpose': skill_data.get('purpose', '')[:2000],
        'Team': skill_data.get('team', 'General'),
        'Content': content_json
    }

    # Add integration if present
    integrations = skill_data.get('integration', [])
    if integrations:
        fields['Integration'] = ', '.join(integrations)

    body = {
        'records': [{'fields': fields}],
        'typecast': True
    }

    try:
        response = make_request_with_retry('POST', url, headers, body)

        if response.status_code == 200:
            data = response.json()
            record_id = data['records'][0]['id']
            return True, record_id
        else:
            error = response.json().get('error', {})
            return False, error.get('message', f'HTTP {response.status_code}')

    except Exception as e:
        return False, str(e)


def sync_notion_to_airtable(base_id, table_id, token_name=None, skill_filter=None,
                             dry_run=False, skip_existing=True, download_files=True):
    """Sync skills from Notion to Airtable.

    Args:
        base_id: Airtable base ID
        table_id: Airtable table ID
        token_name: Airtable token name
        skill_filter: Optional skill name to filter
        dry_run: Don't actually upload
        skip_existing: Skip skills already in Airtable
        download_files: Try to download skill files from Notion

    Returns:
        Tuple of (synced_count, skipped_count, failed_count)
    """
    # Query Notion
    print("Querying Notion Skills database...")
    notion_skills = query_notion_skills(skill_filter)

    if notion_skills is None:
        print("Failed to query Notion")
        return 0, 0, 0

    print(f"Found {len(notion_skills)} skills in Notion")

    # Get existing Airtable skills
    existing = set()
    if skip_existing:
        print("Checking existing Airtable skills...")
        existing = get_existing_airtable_skills(base_id, table_id, token_name)
        print(f"Found {len(existing)} existing skills in Airtable")

    synced = 0
    skipped = 0
    failed = 0

    for skill in notion_skills:
        name = skill.get('skill_name', 'unknown')

        print(f"{name}...", end=' ', flush=True)

        if name in existing:
            print("SKIP (exists)")
            skipped += 1
            continue

        if dry_run:
            print("would sync")
            synced += 1
            continue

        # Download skill file if enabled
        skill_file = None
        if download_files:
            page_id = skill.get('id', '')
            if page_id:
                skill_file = download_notion_skill_file(page_id, name)

        # Create bundle
        bundle = create_skill_bundle_from_notion(skill, skill_file)

        # Upload to Airtable
        success, result = upload_to_airtable(base_id, table_id, skill, bundle, token_name)

        if success:
            has_file = " (with file)" if skill_file else " (metadata only)"
            print(f"OK{has_file}")
            synced += 1
        else:
            print(f"FAILED - {result}")
            failed += 1

    return synced, skipped, failed


def main():
    parser = argparse.ArgumentParser(
        description='Sync skills from Notion to Airtable',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--base', required=True, help='Airtable Base ID')
    parser.add_argument('--table', required=True, help='Airtable Table ID')
    parser.add_argument('--token', required=True, help='Airtable token name (e.g., MUTAGENT)')
    parser.add_argument('--skill', help='Sync specific skill only')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be synced')
    parser.add_argument('--force', action='store_true', help='Sync even if skill exists in Airtable')
    parser.add_argument('--no-files', action='store_true', help='Skip downloading skill files')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    # Load environment
    load_env()

    if not args.json:
        print(f"Using token: AIRTABLE_API_KEY_{args.token.upper()}")
        if args.dry_run:
            print("(dry run - no changes will be made)")

    synced, skipped, failed = sync_notion_to_airtable(
        args.base,
        args.table,
        args.token,
        args.skill,
        args.dry_run,
        skip_existing=not args.force,
        download_files=not args.no_files
    )

    if args.json:
        print(json.dumps({'synced': synced, 'skipped': skipped, 'failed': failed}))
    else:
        print(f"\nDone! {synced} synced, {skipped} skipped, {failed} failed")


if __name__ == '__main__':
    main()
