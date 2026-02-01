#!/usr/bin/env python3
"""
Upload Skill Files to Linked Table

Uploads individual files for large skills to the SkillFiles table,
linked to the main Skills table record.

Usage:
    python upload_skill_files.py --base <BASE_ID> --skills-table <TABLE_ID> \\
        --files-table <TABLE_ID> --token MUTAGENT

    # Upload only partial skills (those missing complete bundles)
    python upload_skill_files.py --base app1gngDx52VAgjVQ \\
        --skills-table tblsQL8n9EfMAFIyD --files-table tblhx8DRvcHN7GWmJ \\
        --token MUTAGENT --partial-only
"""

import os
import sys
import json
import base64
import argparse
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
    import yaml
except ImportError as e:
    print(f'Missing dependency: {e.name}')
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


def get_all_records(base_id, table_id, token_name=None, filter_formula=None):
    """Fetch all records from a table."""
    headers = get_headers(token_name)
    url = f'{API_BASE_URL}/{base_id}/{table_id}'

    records = []
    offset = None

    while True:
        params = {'pageSize': 100}
        if offset:
            params['offset'] = offset
        if filter_formula:
            params['filterByFormula'] = filter_formula

        import urllib.parse
        full_url = f"{url}?{urllib.parse.urlencode(params)}"

        response = make_request_with_retry('GET', full_url, headers)
        if response.status_code != 200:
            print(f'Error fetching records: {response.status_code}')
            return None

        data = response.json()
        records.extend(data.get('records', []))

        offset = data.get('offset')
        if not offset:
            break

    return records


def find_skill_path(skill_name, skills_root):
    """Find local skill path by name."""
    skills_root = Path(skills_root)

    # Special cases for name mismatches
    name_map = {
        'google-integration': 'google',
    }
    skill_name = name_map.get(skill_name, skill_name)

    for skill_md in skills_root.rglob('SKILL.md'):
        parent = skill_md.parent

        # Check if name matches
        if parent.name == skill_name:
            return parent

        # Check nested path pattern (e.g., hubspot/hubspot-connect)
        if '/' in skill_name:
            parts = skill_name.split('/')
            if len(parts) == 2 and parent.name == parts[1]:
                return parent

    return None


def get_file_type(file_path):
    """Get file type category from extension."""
    ext = Path(file_path).suffix.lower().lstrip('.')
    type_map = {
        'py': 'py',
        'md': 'md',
        'json': 'json',
        'yaml': 'yaml',
        'yml': 'yaml',
        'txt': 'txt',
    }
    return type_map.get(ext, 'other')


def upload_file_record(base_id, files_table, skill_record_id, file_path, rel_path, token_name=None):
    """Upload a single file record to SkillFiles table."""
    headers = get_headers(token_name)
    url = f'{API_BASE_URL}/{base_id}/{files_table}'

    # Read and encode file
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        content_b64 = base64.b64encode(content).decode('utf-8')
        file_size = len(content)
    except Exception as e:
        return False, f"Read error: {e}"

    # Check size limit
    if len(content_b64) > 90000:
        return False, f"File too large ({len(content_b64)} bytes encoded)"

    fields = {
        'FilePath': rel_path,
        'Content': content_b64,
        'FileSize': file_size,
        'FileType': get_file_type(rel_path),
        'Skill': [skill_record_id]  # Link to parent skill
    }

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


def upload_skill_files(base_id, files_table, skill_record_id, skill_name, skill_path, token_name=None):
    """Upload all files for a skill to the SkillFiles table."""
    skill_path = Path(skill_path)
    uploaded = 0
    failed = 0
    skipped = 0

    for file_path in skill_path.rglob('*'):
        if not file_path.is_file():
            continue

        rel_path = str(file_path.relative_to(skill_path)).replace('\\', '/')

        # Skip cache files
        if '__pycache__' in rel_path or '.pyc' in rel_path:
            continue

        success, result = upload_file_record(
            base_id, files_table, skill_record_id, file_path, rel_path, token_name
        )

        if success:
            uploaded += 1
        elif 'too large' in result.lower():
            skipped += 1
            print(f"     Skip {rel_path}: too large")
        else:
            failed += 1
            print(f"     FAIL {rel_path}: {result}")

    return uploaded, failed, skipped


def main():
    parser = argparse.ArgumentParser(description='Upload skill files to linked table')
    parser.add_argument('--base', required=True, help='Base ID')
    parser.add_argument('--skills-table', required=True, help='Skills table ID')
    parser.add_argument('--files-table', required=True, help='SkillFiles table ID')
    parser.add_argument('--token', required=True, help='Token name (e.g., MUTAGENT)')
    parser.add_argument('--partial-only', action='store_true', help='Only upload skills with partial bundles')
    parser.add_argument('--skill', help='Upload files for specific skill only')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be uploaded')
    parser.add_argument('--limit', type=int, help='Limit number of skills')

    args = parser.parse_args()

    # Load environment
    load_env()

    skills_root = Path(NEXUS_ROOT) / '00-system' / 'skills'

    print(f"Using token: AIRTABLE_API_KEY_{args.token.upper()}")
    print(f"Fetching skills from Airtable...")

    # Get all skill records
    records = get_all_records(args.base, args.skills_table, args.token)
    if records is None:
        print("Failed to fetch records")
        sys.exit(1)

    print(f"Found {len(records)} skill records")

    # Filter to partial bundles if requested
    skills_to_process = []
    for rec in records:
        fields = rec.get('fields', {})
        name = fields.get('Name', '')
        content = fields.get('Content', '')

        if args.skill and name != args.skill:
            continue

        if args.partial_only:
            try:
                bundle = json.loads(content) if content else {}
                if not bundle.get('partial', False):
                    continue
            except:
                continue

        skills_to_process.append({
            'record_id': rec['id'],
            'name': name,
            'content': content
        })

    if args.limit:
        skills_to_process = skills_to_process[:args.limit]

    print(f"Processing {len(skills_to_process)} skills")

    if args.dry_run:
        print("\nDry run - would upload files for:")
        for skill in skills_to_process:
            skill_path = find_skill_path(skill['name'], skills_root)
            if skill_path:
                file_count = sum(1 for f in skill_path.rglob('*') if f.is_file() and '__pycache__' not in str(f))
                print(f"  {skill['name']}: {file_count} files")
            else:
                print(f"  {skill['name']}: LOCAL NOT FOUND")
        return

    # Process each skill
    total_uploaded = 0
    total_failed = 0
    total_skipped = 0

    for i, skill in enumerate(skills_to_process, 1):
        name = skill['name']
        record_id = skill['record_id']

        print(f"[{i}/{len(skills_to_process)}] {name}...", end=' ', flush=True)

        # Find local skill path
        skill_path = find_skill_path(name, skills_root)
        if not skill_path:
            print("LOCAL NOT FOUND")
            total_failed += 1
            continue

        # Upload files
        uploaded, failed, skipped = upload_skill_files(
            args.base, args.files_table, record_id, name, skill_path, args.token
        )

        total_uploaded += uploaded
        total_failed += failed
        total_skipped += skipped

        print(f"{uploaded} files uploaded" + (f", {skipped} skipped" if skipped else ""))

    print(f"\nDone! {total_uploaded} files uploaded, {total_failed} failed, {total_skipped} skipped")


if __name__ == '__main__':
    main()
