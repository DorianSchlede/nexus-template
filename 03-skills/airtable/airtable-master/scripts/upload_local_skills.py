#!/usr/bin/env python3
"""
Upload Local Skills to Airtable

Finds all local SKILL.md files and uploads them to Airtable with JSON bundles.

Usage:
    python upload_local_skills.py --base <BASE_ID> --table <TABLE_ID> --token <TOKEN>

Example:
    python upload_local_skills.py --base app1gngDx52VAgjVQ --table tblsQL8n9EfMAFIyD --token MUTAGENT
"""

import os
import sys
import json
import base64
import argparse
import re
from pathlib import Path
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
    print("Error: Could not find Nexus root")
    sys.exit(1)

sys.path.insert(0, NEXUS_ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import yaml
    import requests
except ImportError as e:
    print(f"Missing dependency: {e.name}")
    print(f"Run: pip install {e.name}")
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
                print(f"   Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            return response
        return response


API_BASE_URL = 'https://api.airtable.com/v0'
MAX_CONTENT_SIZE = 90000  # Airtable limit ~100KB, leave margin


def parse_yaml_frontmatter(content):
    """Extract YAML frontmatter from markdown content."""
    if not content.startswith('---'):
        return {}, content

    lines = content.split('\n')
    end_idx = -1
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == '---':
            end_idx = i
            break

    if end_idx == -1:
        return {}, content

    yaml_content = '\n'.join(lines[1:end_idx])
    remaining = '\n'.join(lines[end_idx+1:])

    try:
        metadata = yaml.safe_load(yaml_content) or {}
        return metadata, remaining
    except yaml.YAMLError:
        return {}, content


def find_skill_files(skill_path):
    """Find all files in a skill directory."""
    skill_path = Path(skill_path)
    files = {}

    for file_path in skill_path.rglob('*'):
        if file_path.is_file():
            # Get relative path and normalize separators
            rel_path = str(file_path.relative_to(skill_path)).replace('\\', '/')

            # Skip cache and compiled files
            if '__pycache__' in rel_path or '.pyc' in rel_path:
                continue

            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                files[rel_path] = base64.b64encode(content).decode('utf-8')
            except Exception as e:
                print(f"   Warning: Could not read {rel_path}: {e}")

    return files


def create_skill_bundle(skill_path, metadata, skill_md_only=False):
    """Create a JSON bundle for a skill.

    Args:
        skill_path: Path to skill directory
        metadata: Skill metadata from frontmatter
        skill_md_only: If True, only include SKILL.md (for large skills)
    """
    if skill_md_only:
        # Only include SKILL.md for large skills
        skill_md_path = Path(skill_path) / 'SKILL.md'
        files = {}
        if skill_md_path.exists():
            with open(skill_md_path, 'rb') as f:
                files['SKILL.md'] = base64.b64encode(f.read()).decode('utf-8')
    else:
        files = find_skill_files(skill_path)

    bundle = {
        "skill_name": metadata.get('name', Path(skill_path).name),
        "version": metadata.get('version', '1.0'),
        "bundle_format": "nexus-skill-bundle-v1",
        "created": datetime.now().isoformat(),
        "files": files,
        "partial": skill_md_only  # Flag to indicate partial bundle
    }

    return bundle


def get_skill_name_from_path(skill_path):
    """Extract skill name from path."""
    parts = Path(skill_path).parts
    # Find the skills directory and get the name after it
    for i, part in enumerate(parts):
        if part == 'skills' and i < len(parts) - 1:
            # Return last two parts (category/skill-name)
            remaining = parts[i+1:]
            if len(remaining) >= 2:
                return f"{remaining[-2]}/{remaining[-1]}"
            elif len(remaining) == 1:
                return remaining[0]
    return Path(skill_path).name


def find_all_skills(skills_root):
    """Find all SKILL.md files and return skill info."""
    skills = []
    skills_root = Path(skills_root)

    for skill_md in skills_root.rglob('SKILL.md'):
        skill_path = skill_md.parent

        try:
            with open(skill_md, 'r', encoding='utf-8') as f:
                content = f.read()

            metadata, _ = parse_yaml_frontmatter(content)

            skill_info = {
                'path': str(skill_path),
                'skill_md': str(skill_md),
                'name': metadata.get('name', get_skill_name_from_path(skill_path)),
                'description': metadata.get('description', ''),
                'version': metadata.get('version', '1.0'),
                'metadata': metadata
            }

            skills.append(skill_info)

        except Exception as e:
            print(f"Warning: Could not parse {skill_md}: {e}")

    return skills


def upload_skill_to_airtable(base_id, table_id, skill_info, token_name=None):
    """Upload a single skill to Airtable."""
    headers = get_headers(token_name)
    url = f"{API_BASE_URL}/{base_id}/{table_id}"

    # Create the JSON bundle - first try full bundle
    bundle = create_skill_bundle(skill_info['path'], skill_info['metadata'], skill_md_only=False)
    bundle_json = json.dumps(bundle, ensure_ascii=False)

    # If too large, fall back to SKILL.md only
    is_partial = False
    if len(bundle_json) > MAX_CONTENT_SIZE:
        bundle = create_skill_bundle(skill_info['path'], skill_info['metadata'], skill_md_only=True)
        bundle_json = json.dumps(bundle, ensure_ascii=False)
        is_partial = True

    # Extract team/integration from path
    path_parts = Path(skill_info['path']).parts
    team = None

    for i, part in enumerate(path_parts):
        if part == 'skills' and i < len(path_parts) - 1:
            team = path_parts[i+1] if i+1 < len(path_parts) else None
            break

    # Build record fields
    fields = {
        "Name": skill_info['name'],
        "Description": skill_info.get('description', '')[:10000],  # Airtable limit
        "Version": str(skill_info.get('version', '1.0')),
        "Content": bundle_json
    }

    # Add team if found
    if team:
        fields["Team"] = team

    # Add purpose from metadata if available
    purpose = skill_info['metadata'].get('purpose', '')
    if purpose:
        fields["Purpose"] = purpose[:10000]

    body = {
        "records": [{"fields": fields}],
        "typecast": True
    }

    try:
        response = make_request_with_retry('POST', url, headers, body)

        if response.status_code == 200:
            data = response.json()
            record_id = data['records'][0]['id']
            status = f"{record_id} (partial)" if is_partial else record_id
            return True, status
        else:
            error = response.json().get('error', {})
            return False, error.get('message', f'HTTP {response.status_code}')

    except Exception as e:
        return False, str(e)


def main():
    parser = argparse.ArgumentParser(description='Upload local skills to Airtable')
    parser.add_argument('--base', required=True, help='Base ID (appXXX)')
    parser.add_argument('--table', required=True, help='Table ID or name')
    parser.add_argument('--token', help='Token name (e.g., MUTAGENT)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be uploaded')
    parser.add_argument('--limit', type=int, help='Limit number of uploads')
    parser.add_argument('--filter', help='Only upload skills matching pattern (e.g., "master")')

    args = parser.parse_args()

    # Load environment
    load_env()

    # Find skills directory
    skills_root = Path(NEXUS_ROOT) / '00-system' / 'skills'

    if not skills_root.exists():
        print(f"Error: Skills directory not found: {skills_root}")
        sys.exit(1)

    print(f"Scanning {skills_root}...")
    skills = find_all_skills(skills_root)
    print(f"Found {len(skills)} skills")

    # Filter skills if pattern specified
    if args.filter:
        pattern = args.filter.lower()
        skills = [s for s in skills if pattern in s['name'].lower() or pattern in s['path'].lower()]
        print(f"Filtered to {len(skills)} skills matching '{args.filter}'")

    if args.limit:
        skills = skills[:args.limit]
        print(f"Limited to {len(skills)} skills")

    if args.dry_run:
        print("\nDry run - would upload:")
        for skill in skills:
            print(f"  - {skill['name']} (v{skill['version']})")
        return

    # Upload skills
    success_count = 0
    fail_count = 0

    print(f"\nUploading to Airtable...")
    if args.token:
        print(f"Using token: AIRTABLE_API_KEY_{args.token.upper()}")

    for i, skill in enumerate(skills, 1):
        name = skill['name']
        print(f"[{i}/{len(skills)}] {name}...", end=' ', flush=True)

        success, result = upload_skill_to_airtable(
            args.base,
            args.table,
            skill,
            args.token
        )

        if success:
            print(f"OK ({result})")
            success_count += 1
        else:
            print(f"FAILED: {result}")
            fail_count += 1

    print(f"\nDone! {success_count} uploaded, {fail_count} failed")


if __name__ == '__main__':
    main()
