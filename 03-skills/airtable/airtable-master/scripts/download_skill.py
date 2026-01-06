#!/usr/bin/env python3
"""
Download Skills from Airtable

Downloads skill bundles from Airtable and extracts them to local filesystem.
Supports linked SkillFiles table for partial bundles.

Usage:
    python download_skill.py --base <BASE_ID> --table <TABLE_ID> --skill <SKILL_NAME> --token <TOKEN>
    python download_skill.py --base <BASE_ID> --table <TABLE_ID> --all --token <TOKEN>

Examples:
    # Download single skill
    python download_skill.py --base app1gngDx52VAgjVQ --table tblsQL8n9EfMAFIyD \\
        --skill "gmail" --token MUTAGENT

    # Download all skills (including linked files for partial bundles)
    python download_skill.py --base app1gngDx52VAgjVQ --table tblsQL8n9EfMAFIyD \\
        --files-table tblhx8DRvcHN7GWmJ --all --token MUTAGENT --output ./downloaded-skills

    # Dry run - show what would be downloaded
    python download_skill.py --base app1gngDx52VAgjVQ --table tblsQL8n9EfMAFIyD \\
        --all --token MUTAGENT --dry-run
"""

import os
import sys
import json
import base64
import argparse
import shutil
from pathlib import Path
from datetime import datetime

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
    print('Run: pip install requests')
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


def get_all_records(base_id, table_id, token_name=None, filter_formula=None):
    """Fetch all records from Airtable table."""
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

        # Build URL with params
        import urllib.parse
        full_url = f"{url}?{urllib.parse.urlencode(params)}"

        response = make_request_with_retry('GET', full_url, headers)
        if response.status_code == 429:
            import time
            time.sleep(30)
            continue

        if response.status_code != 200:
            print(f'Error fetching records: {response.status_code}')
            return None

        data = response.json()
        records.extend(data.get('records', []))

        offset = data.get('offset')
        if not offset:
            break

    return records


def extract_bundle(bundle_json, output_dir, skill_name, backup=True):
    """Extract a skill bundle to the filesystem.

    Args:
        bundle_json: JSON string containing the bundle
        output_dir: Directory to extract to
        skill_name: Name of the skill
        backup: Create backup of existing skill if True

    Returns:
        Tuple of (success, message)
    """
    try:
        bundle = json.loads(bundle_json)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"

    files = bundle.get('files', {})
    if not files:
        return False, "No files in bundle"

    is_partial = bundle.get('partial', False)
    skill_dir = Path(output_dir) / skill_name

    # Backup existing skill
    if skill_dir.exists() and backup:
        backup_dir = skill_dir.parent / f"{skill_name}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.move(str(skill_dir), str(backup_dir))
        print(f"   Backed up existing skill to {backup_dir.name}")

    # Create skill directory
    skill_dir.mkdir(parents=True, exist_ok=True)

    # Extract files
    extracted = 0
    for rel_path, content_b64 in files.items():
        try:
            content = base64.b64decode(content_b64)
            file_path = skill_dir / rel_path

            # Create parent directories
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            with open(file_path, 'wb') as f:
                f.write(content)
            extracted += 1
        except Exception as e:
            print(f"   Warning: Failed to extract {rel_path}: {e}")

    status = "partial" if is_partial else "complete"
    return True, f"Extracted {extracted} files ({status})"


def get_linked_files(base_id, files_table, skill_record_id, token_name=None):
    """Fetch linked files for a skill from SkillFiles table.

    Args:
        base_id: Airtable base ID
        files_table: SkillFiles table ID
        skill_record_id: Record ID of the parent skill
        token_name: API token name

    Returns:
        Dict mapping file paths to base64 content, or None on error
    """
    # Airtable's filter formula doesn't work well with linked record arrays
    # So we fetch all records and filter client-side
    records = get_all_records(base_id, files_table, token_name)

    if records is None:
        return None

    files = {}
    for rec in records:
        fields = rec.get('fields', {})
        # Skill field is an array of linked record IDs
        linked_skills = fields.get('Skill', [])

        # Check if this file belongs to our skill
        if skill_record_id in linked_skills:
            file_path = fields.get('FilePath', '')
            content = fields.get('Content', '')

            if file_path and content:
                files[file_path] = content

    return files


def download_skill_with_linked(base_id, table_id, skill_name, output_dir,
                                token_name=None, files_table=None, backup=True):
    """Download a skill, including linked files for partial bundles.

    Args:
        base_id: Airtable base ID
        table_id: Skills table ID
        skill_name: Name of skill to download
        output_dir: Output directory
        token_name: API token name
        files_table: SkillFiles table ID (optional)
        backup: Create backup of existing skill

    Returns:
        Tuple of (success, message)
    """
    # Find the skill record
    filter_formula = f'{{Name}}="{skill_name}"'
    records = get_all_records(base_id, table_id, token_name, filter_formula)

    if not records:
        return False, "Skill not found"

    if len(records) > 1:
        return False, f"Multiple skills found with name '{skill_name}'"

    record = records[0]
    record_id = record['id']
    fields = record.get('fields', {})
    content = fields.get('Content', '')

    if not content:
        return False, "No content in skill record"

    # Parse bundle
    try:
        bundle = json.loads(content)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"

    is_partial = bundle.get('partial', False)

    # If partial and files_table provided, fetch linked files
    if is_partial and files_table:
        linked_files = get_linked_files(base_id, files_table, record_id, token_name)
        if linked_files:
            # Merge linked files into bundle
            bundle['files'].update(linked_files)
            bundle['partial'] = False  # Now complete

    # Extract bundle
    skill_dir = Path(output_dir) / skill_name

    # Backup existing skill
    if skill_dir.exists() and backup:
        backup_dir = skill_dir.parent / f"{skill_name}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.move(str(skill_dir), str(backup_dir))
        print(f"   Backed up existing skill to {backup_dir.name}")

    # Create skill directory
    skill_dir.mkdir(parents=True, exist_ok=True)

    # Extract files
    files = bundle.get('files', {})
    extracted = 0
    for rel_path, content_b64 in files.items():
        try:
            file_content = base64.b64decode(content_b64)
            file_path = skill_dir / rel_path

            # Create parent directories
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            with open(file_path, 'wb') as f:
                f.write(file_content)
            extracted += 1
        except Exception as e:
            print(f"   Warning: Failed to extract {rel_path}: {e}")

    status = "complete" if not bundle.get('partial', False) else "partial"
    linked_count = len(linked_files) if is_partial and files_table and linked_files else 0
    if linked_count:
        return True, f"Extracted {extracted} files ({status}, +{linked_count} linked)"
    return True, f"Extracted {extracted} files ({status})"


def download_skill(base_id, table_id, skill_name, output_dir, token_name=None, backup=True):
    """Download a single skill from Airtable."""
    # Find the skill record
    filter_formula = f'{{Name}}="{skill_name}"'
    records = get_all_records(base_id, table_id, token_name, filter_formula)

    if not records:
        return False, "Skill not found"

    if len(records) > 1:
        return False, f"Multiple skills found with name '{skill_name}'"

    record = records[0]
    fields = record.get('fields', {})
    content = fields.get('Content', '')

    if not content:
        return False, "No content in skill record"

    return extract_bundle(content, output_dir, skill_name, backup)


def download_all_skills(base_id, table_id, output_dir, token_name=None,
                        files_table=None, backup=True, dry_run=False):
    """Download all skills from Airtable.

    Args:
        base_id: Airtable base ID
        table_id: Skills table ID
        output_dir: Output directory
        token_name: API token name
        files_table: SkillFiles table ID for linked files (optional)
        backup: Create backup of existing skills
        dry_run: Only show what would be downloaded

    Returns:
        Tuple of (success_count, fail_count)
    """
    records = get_all_records(base_id, table_id, token_name)

    if records is None:
        return 0, 0

    success_count = 0
    fail_count = 0

    for record in records:
        record_id = record['id']
        fields = record.get('fields', {})
        name = fields.get('Name', 'unknown')
        content = fields.get('Content', '')

        print(f"{name}...", end=' ', flush=True)

        if not content:
            print("SKIP (no content)")
            fail_count += 1
            continue

        if dry_run:
            try:
                bundle = json.loads(content)
                files = bundle.get('files', {})
                is_partial = bundle.get('partial', False)
                status = "partial" if is_partial else "complete"
                if is_partial and files_table:
                    print(f"would extract {len(files)} files ({status}) + linked files")
                else:
                    print(f"would extract {len(files)} files ({status})")
                success_count += 1
            except:
                print("INVALID JSON")
                fail_count += 1
            continue

        # Use linked mode if files_table provided
        if files_table:
            success, message = download_skill_with_linked(
                base_id, table_id, name, output_dir, token_name, files_table, backup
            )
        else:
            success, message = extract_bundle(content, output_dir, name, backup)

        if success:
            print(f"OK - {message}")
            success_count += 1
        else:
            print(f"FAILED - {message}")
            fail_count += 1

    return success_count, fail_count


def main():
    parser = argparse.ArgumentParser(
        description='Download skills from Airtable',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--base', required=True, help='Base ID (appXXX)')
    parser.add_argument('--table', required=True, help='Table ID or name')
    parser.add_argument('--files-table', help='SkillFiles table ID for linked files')
    parser.add_argument('--token', help='Token name (e.g., MUTAGENT)')
    parser.add_argument('--skill', help='Skill name to download')
    parser.add_argument('--all', action='store_true', help='Download all skills')
    parser.add_argument('--output', default='./downloaded-skills', help='Output directory')
    parser.add_argument('--no-backup', action='store_true', help='Skip backup of existing skills')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be downloaded')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    if not args.skill and not args.all:
        parser.error("Must specify --skill or --all")

    # Load environment
    load_env()

    output_dir = Path(args.output)
    backup = not args.no_backup

    if args.token and not args.json:
        print(f"Using token: AIRTABLE_API_KEY_{args.token.upper()}")
    if args.files_table and not args.json:
        print(f"Using linked files table: {args.files_table}")

    if args.all:
        if not args.json:
            print(f"Downloading all skills to {output_dir}...")
            if args.dry_run:
                print("(dry run - no files will be written)")

        success, failed = download_all_skills(
            args.base, args.table, output_dir, args.token,
            args.files_table, backup, args.dry_run
        )

        if args.json:
            print(json.dumps({'success': success, 'failed': failed}))
        else:
            print(f"\nDone! {success} downloaded, {failed} failed/skipped")

    else:
        if not args.json:
            print(f"Downloading skill '{args.skill}' to {output_dir}...")

        if args.dry_run:
            # Just check if skill exists
            filter_formula = f'{{Name}}="{args.skill}"'
            records = get_all_records(args.base, args.table, args.token, filter_formula)
            if records:
                bundle = json.loads(records[0].get('fields', {}).get('Content', '{}'))
                files = bundle.get('files', {})
                is_partial = bundle.get('partial', False)
                if is_partial and args.files_table:
                    print(f"Would extract {len(files)} files (partial) + linked files")
                else:
                    print(f"Would extract {len(files)} files")
            else:
                print("Skill not found")
        else:
            # Use linked mode if files_table provided
            if args.files_table:
                success, message = download_skill_with_linked(
                    args.base, args.table, args.skill, output_dir,
                    args.token, args.files_table, backup
                )
            else:
                success, message = download_skill(
                    args.base, args.table, args.skill, output_dir, args.token, backup
                )

            if args.json:
                print(json.dumps({'success': success, 'message': message}))
            else:
                if success:
                    print(f"OK - {message}")
                else:
                    print(f"FAILED - {message}")
                    sys.exit(1)


if __name__ == '__main__':
    main()
