#!/usr/bin/env python3
"""
Update Skill Metadata in Airtable

Extracts additional metadata from SKILL.md files and updates existing Airtable records.
Extracts: Purpose, Trigger Phrases, Workflows

Usage:
    python update_skill_metadata.py --base <BASE_ID> --table <TABLE_ID> --token <TOKEN>
"""

import os
import sys
import json
import re
import requests
from pathlib import Path
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
    print('Could not find Nexus root')
    sys.exit(1)

# Load .env
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


def extract_section(content, section_name):
    """Extract content from a markdown section."""
    # Match ## Section Name and capture until next ## or end
    pattern = rf'^## {re.escape(section_name)}\s*\n(.*?)(?=^## |\Z)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


def extract_purpose(content):
    """Extract purpose from SKILL.md - check ## Purpose section first, then # heading."""
    # Try ## Purpose section
    purpose = extract_section(content, 'Purpose')
    if purpose:
        return purpose[:5000]  # Limit size

    # Try first paragraph after # heading
    lines = content.split('\n')
    in_content = False
    purpose_lines = []

    for line in lines:
        if line.startswith('# ') and not line.startswith('## '):
            in_content = True
            continue
        if in_content:
            if line.startswith('## ') or line.startswith('---'):
                break
            if line.strip():
                purpose_lines.append(line)
            elif purpose_lines:  # Empty line after content = end of intro
                break

    if purpose_lines:
        return '\n'.join(purpose_lines)[:5000]

    return None


def extract_triggers(content):
    """Extract trigger phrases from SKILL.md."""
    triggers = extract_section(content, 'Trigger Phrases')
    if triggers:
        return triggers[:2000]

    # Also check for "Triggers" in workflow sections
    pattern = r'\*\*Triggers?\*\*:\s*([^\n]+)'
    matches = re.findall(pattern, content)
    if matches:
        return ', '.join(matches)[:2000]

    return None


def get_all_records(base_id, table_id, token_name=None):
    """Fetch all records from Airtable table."""
    headers = get_headers(token_name)
    url = f'https://api.airtable.com/v0/{base_id}/{table_id}'

    records = []
    offset = None

    while True:
        params = {'pageSize': 100}
        if offset:
            params['offset'] = offset

        response = requests.get(url, headers=headers, params=params, timeout=30)

        if response.status_code == 429:
            print('Rate limited, waiting...')
            time.sleep(30)
            continue

        if response.status_code != 200:
            print(f'Error fetching records: {response.status_code}')
            break

        data = response.json()
        records.extend(data.get('records', []))

        offset = data.get('offset')
        if not offset:
            break

    return records


def find_skill_file(skill_name, skills_root):
    """Find SKILL.md file for a skill name."""
    skills_root = Path(skills_root)

    # Try exact match first
    for skill_md in skills_root.rglob('SKILL.md'):
        parent = skill_md.parent
        if parent.name == skill_name:
            return skill_md
        # Check category/skill-name pattern
        if skill_name in str(skill_md):
            return skill_md

    return None


def update_record(base_id, table_id, record_id, fields, token_name=None):
    """Update a single Airtable record."""
    headers = get_headers(token_name)
    url = f'https://api.airtable.com/v0/{base_id}/{table_id}/{record_id}'

    body = {'fields': fields}

    response = requests.patch(url, headers=headers, json=body, timeout=30)

    if response.status_code == 429:
        time.sleep(30)
        response = requests.patch(url, headers=headers, json=body, timeout=30)

    return response.status_code == 200


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Update skill metadata in Airtable')
    parser.add_argument('--base', required=True, help='Base ID')
    parser.add_argument('--table', required=True, help='Table ID')
    parser.add_argument('--token', help='Token name')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be updated')

    args = parser.parse_args()

    skills_root = Path(NEXUS_ROOT) / '00-system' / 'skills'

    print(f'Fetching records from Airtable...')
    records = get_all_records(args.base, args.table, args.token)
    print(f'Found {len(records)} records')

    updated = 0
    skipped = 0

    for rec in records:
        record_id = rec['id']
        fields = rec.get('fields', {})
        name = fields.get('Name', '')

        # Find the skill file
        skill_md = find_skill_file(name, skills_root)
        if not skill_md:
            print(f'{name}: SKILL.md not found, skipping')
            skipped += 1
            continue

        # Read content
        try:
            with open(skill_md, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f'{name}: Error reading file: {e}')
            skipped += 1
            continue

        # Extract metadata
        purpose = extract_purpose(content)
        triggers = extract_triggers(content)

        # Build update fields
        update_fields = {}

        if purpose and not fields.get('Purpose'):
            update_fields['Purpose'] = purpose

        # Skip if nothing to update
        if not update_fields:
            skipped += 1
            continue

        print(f'{name}...', end=' ', flush=True)

        if args.dry_run:
            print(f'would update: {list(update_fields.keys())}')
            updated += 1
        else:
            if update_record(args.base, args.table, record_id, update_fields, args.token):
                print(f'OK (updated {list(update_fields.keys())})')
                updated += 1
            else:
                print('FAILED')
                skipped += 1

    print(f'\nDone! {updated} updated, {skipped} skipped')


if __name__ == '__main__':
    main()
