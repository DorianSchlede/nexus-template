#!/usr/bin/env python3
"""
DEPRECATED: Use Airtable Skill Marketplace instead.

For skill upload, use:
    python 00-system/skills/airtable/airtable-master/scripts/upload_local_skills.py \
        --base app1gngDx52VAgjVQ --table tblsQL8n9EfMAFIyD --token MUTAGENT

---

Upload Skill to Notion - Creates database entry with JSON bundle attachment (LEGACY)

Packages entire skill folder (SKILL.md + scripts/ + references/ + assets/) into a
JSON bundle with base64-encoded files, then uploads via Notion File Upload API.

Usage:
    python upload_skill.py <skill_path> --team TEAM [--integration INT1,INT2]
    python upload_skill.py <skill_path> --team TEAM --dry-run
    python upload_skill.py <skill_path> --team TEAM --as-new "skill-name-v2"

Examples:
    python upload_skill.py 03-skills/my-skill --team General
    python upload_skill.py 03-skills/beam-agents --team Solutions --integration "Beam AI"
    python upload_skill.py 03-skills/my-skill --team General --dry-run
    python upload_skill.py 03-skills/my-skill --team General --as-new "my-skill-enhanced"

Returns:
    Exit code 0 if successful, 1 if error
"""

import sys
import os
import json
import argparse
import re
import base64
from pathlib import Path
from datetime import date

try:
    import requests
    import yaml
except ImportError:
    print("[ERROR] Missing dependencies")
    print("Install with: pip install requests pyyaml")
    sys.exit(1)


def find_nexus_root():
    """Find Nexus root directory"""
    current = Path.cwd()
    for path in [current] + list(current.parents):
        if (path / 'CLAUDE.md').exists():
            return path
    return current


def load_env_file(env_path):
    """Load .env file"""
    env_vars = {}
    if not env_path.exists():
        return env_vars

    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip().strip('"').strip("'")

    return env_vars


def load_user_config(config_path):
    """Load user-config.yaml"""
    if not config_path.exists():
        return {}

    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Handle YAML frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            yaml_content = parts[1] if len(parts) >= 2 else content
        else:
            yaml_content = content

        try:
            return yaml.safe_load(yaml_content) or {}
        except yaml.YAMLError:
            return {}


def validate_skill_md(skill_path):
    """
    Validate SKILL.md before export

    Returns:
        Tuple of (is_valid, errors_list)
    """
    skill_md = skill_path / 'SKILL.md'
    errors = []

    if not skill_md.exists():
        return False, ["SKILL.md not found"]

    content = skill_md.read_text(encoding='utf-8')

    # Check YAML frontmatter exists
    if not content.startswith('---'):
        errors.append("Missing YAML frontmatter (must start with ---)")
        return False, errors

    # Extract and validate YAML
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if not match:
        errors.append("Invalid YAML frontmatter format (missing closing ---)")
        return False, errors

    frontmatter_text = match.group(1)

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML syntax: {e}")
        return False, errors

    # Check required fields
    if not frontmatter.get("name"):
        errors.append("Missing required field: name")

    if not frontmatter.get("description"):
        errors.append("Missing required field: description")

    # Check description has trigger phrases (should contain "when" or "Load when")
    desc = frontmatter.get("description", "")
    if desc and "when" not in desc.lower():
        errors.append("Description should include trigger phrases (e.g., 'Load when user says...')")

    # Validate version format if present
    version = frontmatter.get("version", "1.0")
    if not re.match(r'^\d+\.\d+(\.\d+)?$', str(version)):
        errors.append(f"Invalid version format '{version}' (use semantic versioning like 1.0 or 1.0.0)")

    if errors:
        return False, errors

    return True, []


def read_skill_md(skill_path):
    """
    Read and parse SKILL.md file

    Returns:
        Dict with {name, description, purpose, version, content}
    """
    skill_md = skill_path / 'SKILL.md'

    if not skill_md.exists():
        print(f"[ERROR] SKILL.md not found in {skill_path}", file=sys.stderr)
        return None

    content = skill_md.read_text(encoding='utf-8')

    # Extract YAML frontmatter
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if not match:
        print("[ERROR] Invalid SKILL.md format (missing YAML frontmatter)", file=sys.stderr)
        return None

    frontmatter_text = match.group(1)
    body = match.group(2)

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as e:
        print(f"[ERROR] Invalid YAML frontmatter: {e}", file=sys.stderr)
        return None

    # Extract Purpose section
    purpose_match = re.search(r'^## Purpose\s*\n\n(.+?)(?=\n##|\Z)', body, re.MULTILINE | re.DOTALL)
    purpose = purpose_match.group(1).strip() if purpose_match else ""

    return {
        "name": frontmatter.get("name", ""),
        "description": frontmatter.get("description", ""),
        "version": frontmatter.get("version", "1.0"),
        "purpose": purpose,
        "content": content
    }


def create_skill_bundle(skill_path, version="1.0"):
    """
    Create JSON bundle with all skill files (base64 encoded)

    Structure:
    {
        "skill_name": "my-skill",
        "version": "1.0",
        "bundle_format": "nexus-skill-bundle-v1",
        "created": "2025-12-10",
        "files": {
            "SKILL.md": "<base64>",
            "scripts/script.py": "<base64>",
            "references/guide.md": "<base64>",
            "assets/template.txt": "<base64>"
        }
    }

    Returns:
        Tuple of (bundle_json_string, file_count) or (None, 0) on error
    """
    skill_path = Path(skill_path)
    skill_name = skill_path.name

    # Directories to include
    include_dirs = ['scripts', 'references', 'assets']

    # Files to exclude
    exclude_patterns = ['.DS_Store', '._*', '__pycache__', '*.pyc', '.git']

    def should_exclude(filename):
        for pattern in exclude_patterns:
            if pattern.startswith('*'):
                if filename.endswith(pattern[1:]):
                    return True
            elif pattern.endswith('*'):
                if filename.startswith(pattern[:-1]):
                    return True
            elif filename == pattern:
                return True
        return False

    files = {}

    # Add SKILL.md (required)
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        print(f"[ERROR] SKILL.md not found in {skill_path}", file=sys.stderr)
        return None, 0

    content = skill_md.read_bytes()
    files['SKILL.md'] = base64.b64encode(content).decode('ascii')

    # Add files from subdirectories
    for dir_name in include_dirs:
        dir_path = skill_path / dir_name
        if dir_path.exists() and dir_path.is_dir():
            for file_path in dir_path.rglob('*'):
                if file_path.is_file() and not should_exclude(file_path.name):
                    # Get relative path from skill root
                    rel_path = file_path.relative_to(skill_path)
                    try:
                        content = file_path.read_bytes()
                        files[str(rel_path)] = base64.b64encode(content).decode('ascii')
                    except Exception as e:
                        print(f"[WARN] Could not read {rel_path}: {e}", file=sys.stderr)

    bundle = {
        "skill_name": skill_name,
        "version": version,
        "bundle_format": "nexus-skill-bundle-v1",
        "created": str(date.today()),
        "files": files
    }

    return json.dumps(bundle, indent=2), len(files)


def create_file_upload(api_key, filename, content_type="application/json"):
    """
    Step 1: Create file upload object

    Args:
        api_key: Notion API key
        filename: Name for the uploaded file
        content_type: MIME type (default: application/json for bundles)

    Returns:
        Dict with {id, upload_url} or None
    """
    url = "https://api.notion.com/v1/file_uploads"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    body = {
        "filename": filename,
        "content_type": content_type
    }

    try:
        response = requests.post(url, headers=headers, json=body, timeout=30)

        if response.status_code == 200:
            data = response.json()
            return {
                "id": data.get("id"),
                "upload_url": data.get("upload_url")
            }
        else:
            print(f"[ERROR] Failed to create upload: {response.status_code}", file=sys.stderr)
            print(f"Response: {response.text}", file=sys.stderr)
            return None

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}", file=sys.stderr)
        return None


def upload_file_content(api_key, upload_url, filename, content, content_type="application/json"):
    """
    Step 2: Upload file content

    Args:
        api_key: Notion API key
        upload_url: URL returned from create_file_upload
        filename: Name for the file
        content: File content as string or bytes
        content_type: MIME type

    Returns:
        True if successful
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28"
    }

    # Convert string to bytes if needed
    if isinstance(content, str):
        content = content.encode('utf-8')

    try:
        files = {'file': (filename, content, content_type)}
        response = requests.post(upload_url, headers=headers, files=files, timeout=60)

        if response.status_code == 200:
            data = response.json()
            status = data.get("status")
            if status == "uploaded":
                return True
            else:
                print(f"[ERROR] Upload status: {status}", file=sys.stderr)
                return False
        else:
            print(f"[ERROR] File upload failed: {response.status_code}", file=sys.stderr)
            print(f"Response: {response.text}", file=sys.stderr)
            return False

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}", file=sys.stderr)
        return False


def check_skill_exists(api_key, database_id, skill_name):
    """
    Check if a skill with this name already exists in Notion

    Returns:
        Dict with {exists: bool, page_id: str, url: str, owner: str, version: str} or None on error
    """
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    body = {
        "filter": {
            "property": "Skill Name",
            "title": {"equals": skill_name}
        }
    }

    try:
        response = requests.post(url, headers=headers, json=body, timeout=30)

        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])

            if results:
                page = results[0]
                props = page.get("properties", {})

                # Get owner name
                owner_list = props.get("Owner", {}).get("people", [])
                owner = owner_list[0].get("name", "Unknown") if owner_list else "Unknown"

                # Get version (rich_text type in Notion)
                version_texts = props.get("Version", {}).get("rich_text", [])
                version = version_texts[0].get("plain_text", "1.0") if version_texts else "1.0"

                return {
                    "exists": True,
                    "page_id": page.get("id"),
                    "url": page.get("url"),
                    "owner": owner,
                    "version": version
                }
            else:
                return {"exists": False}
        else:
            print(f"[ERROR] Failed to check duplicates: {response.status_code}", file=sys.stderr)
            return None

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error checking duplicates: {e}", file=sys.stderr)
        return None


def create_database_entry(api_key, database_id, skill_data, file_upload_id, file_name, user_id):
    """
    Step 3: Create database entry with file attachment

    Returns:
        Created page object or None
    """
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    # Build properties
    properties = {
        "Skill Name": {
            "title": [{"text": {"content": skill_data["name"]}}]
        },
        "Description": {
            "rich_text": [{"text": {"content": skill_data["description"]}}]
        },
        "Team": {
            "select": {"name": skill_data["team"]}
        },
        "Created": {
            "date": {"start": str(date.today())}
        },
        "Version": {
            "rich_text": [{"text": {"content": str(skill_data.get("version", "1.0"))}}]
        },
        "Skill": {
            "files": [{
                "type": "file_upload",
                "file_upload": {"id": file_upload_id},
                "name": file_name
            }]
        }
    }

    # Add optional properties
    if skill_data.get("purpose"):
        properties["Purpose"] = {
            "rich_text": [{"text": {"content": skill_data["purpose"]}}]
        }

    if skill_data.get("integrations"):
        properties["Integration"] = {
            "multi_select": [{"name": integ} for integ in skill_data["integrations"]]
        }

    if user_id:
        properties["Owner"] = {
            "people": [{"id": user_id}]
        }

    body = {
        "parent": {"database_id": database_id},
        "properties": properties
    }

    try:
        response = requests.post(url, headers=headers, json=body, timeout=30)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"[ERROR] Failed to create page: {response.status_code}", file=sys.stderr)
            print(f"Response: {response.text}", file=sys.stderr)
            return None

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}", file=sys.stderr)
        return None


def main():
    """Main entry point"""
    # Configure UTF-8 output
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(
        description="Upload skill to Notion database with file attachment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  python upload_skill.py 03-skills/my-skill --team General
  python upload_skill.py 03-skills/beam-agents --team Solutions --integration "Beam AI,Linear"
  python upload_skill.py 03-skills/my-skill --team General --dry-run
  python upload_skill.py 03-skills/my-skill --team General --as-new "my-skill-enhanced"
        """
    )
    parser.add_argument("skill_path", help="Path to skill folder")
    parser.add_argument("--team", required=True, help="Team (General, Solutions, Engineering, Sales)")
    parser.add_argument("--integration", help="Comma-separated integrations (e.g., 'Beam AI,Linear')")
    parser.add_argument("--dry-run", action="store_true", help="Preview upload without actually pushing")
    parser.add_argument("--as-new", metavar="NAME", help="Upload as new skill with different name (for improved versions)")
    parser.add_argument("--skip-validation", action="store_true", help="Skip SKILL.md validation")

    args = parser.parse_args()

    # Validate skill path
    skill_path = Path(args.skill_path).resolve()
    if not skill_path.exists() or not skill_path.is_dir():
        print(f"[ERROR] Skill folder not found: {skill_path}", file=sys.stderr)
        sys.exit(1)

    # Validate SKILL.md before proceeding
    if not args.skip_validation:
        print(f"[INFO] Validating SKILL.md...", file=sys.stderr)
        is_valid, errors = validate_skill_md(skill_path)
        if not is_valid:
            print(f"\n[ERROR] SKILL.md validation failed:", file=sys.stderr)
            for error in errors:
                print(f"  ✗ {error}", file=sys.stderr)
            print(f"\nFix these issues or use --skip-validation to bypass.", file=sys.stderr)
            sys.exit(1)
        print(f"[OK] SKILL.md valid", file=sys.stderr)

    # Read skill metadata
    print(f"[INFO] Reading skill: {skill_path.name}", file=sys.stderr)
    skill_data = read_skill_md(skill_path)

    if not skill_data:
        sys.exit(1)

    # Override name if --as-new provided
    original_name = skill_data["name"]
    if args.as_new:
        skill_data["name"] = args.as_new
        print(f"[INFO] Uploading as new skill: {args.as_new} (based on {original_name})", file=sys.stderr)

    skill_data["team"] = args.team

    if args.integration:
        skill_data["integrations"] = [i.strip() for i in args.integration.split(',')]

    # Find Nexus root and load config
    root = find_nexus_root()
    env_path = root / '.env'
    env_vars = load_env_file(env_path)

    config_path = root / '01-memory' / 'user-config.yaml'
    user_config = load_user_config(config_path)

    # Get credentials
    api_key = env_vars.get('NOTION_API_KEY') or os.getenv('NOTION_API_KEY')
    database_id = env_vars.get('NOTION_SKILLS_DB_ID') or env_vars.get('NOTION_DATABASE_ID')

    # Try multiple paths for user_id (check root level first, then fallbacks)
    user_id = (
        user_config.get('notion_user_id') or  # Root level (preferred, set by setup_notion.py)
        user_config.get('integrations', {}).get('notion', {}).get('user_id') or  # Structured path
        user_config.get('user_preferences', {}).get('notion_user_id')  # Legacy path
    )
    user_name = (
        user_config.get('notion_user_name') or
        user_config.get('integrations', {}).get('notion', {}).get('user_name') or
        user_config.get('user_preferences', {}).get('notion_user_name', 'Unknown')
    )

    if not api_key:
        print("[ERROR] NOTION_API_KEY not found", file=sys.stderr)
        sys.exit(1)

    if not database_id:
        print("[ERROR] NOTION_SKILLS_DB_ID not found", file=sys.stderr)
        sys.exit(1)

    if not user_id:
        print("[WARN] notion_user_id not set in user-config.yaml", file=sys.stderr)
        print("[WARN] Owner field will not be set", file=sys.stderr)

    # Check for duplicate skill name in Notion
    print(f"[INFO] Checking for duplicates...", file=sys.stderr)
    existing = check_skill_exists(api_key, database_id, skill_data["name"])

    if existing is None:
        print("[ERROR] Could not check for duplicates", file=sys.stderr)
        sys.exit(1)

    if existing.get("exists"):
        print(f"\n[ERROR] Skill '{skill_data['name']}' already exists in Notion!", file=sys.stderr)
        print(f"  Owner: {existing['owner']}", file=sys.stderr)
        print(f"  Version: {existing['version']}", file=sys.stderr)
        print(f"  URL: {existing['url']}", file=sys.stderr)
        print(f"\nOptions:", file=sys.stderr)
        print(f"  1. Use --as-new \"new-name\" to upload as improved version", file=sys.stderr)
        print(f"  2. Delete existing skill in Notion first", file=sys.stderr)
        sys.exit(1)

    print(f"[OK] No duplicate found", file=sys.stderr)

    # Create JSON bundle with all skill files
    print(f"[INFO] Creating JSON bundle...", file=sys.stderr)
    bundle_json, file_count = create_skill_bundle(skill_path, skill_data.get("version", "1.0"))

    if not bundle_json:
        sys.exit(1)

    bundle_size = len(bundle_json.encode('utf-8'))
    file_name = f"{skill_data['name']}.skill.json"

    # Show preview
    print(f"\n{'='*50}", file=sys.stderr)
    print(f"[PREVIEW] Upload Summary", file=sys.stderr)
    print(f"{'='*50}", file=sys.stderr)
    print(f"  Skill Name:  {skill_data['name']}", file=sys.stderr)
    print(f"  Version:     {skill_data.get('version', '1.0')}", file=sys.stderr)
    print(f"  Team:        {skill_data['team']}", file=sys.stderr)
    print(f"  Owner:       {user_name}", file=sys.stderr)
    if skill_data.get("integrations"):
        print(f"  Integrations: {', '.join(skill_data['integrations'])}", file=sys.stderr)
    print(f"  Bundle:      {file_name}", file=sys.stderr)
    print(f"  Size:        {bundle_size:,} bytes", file=sys.stderr)
    print(f"  Files:       {file_count}", file=sys.stderr)
    print(f"{'='*50}", file=sys.stderr)

    # If dry-run, stop here
    if args.dry_run:
        print(f"\n[DRY-RUN] No changes made. Remove --dry-run to upload.", file=sys.stderr)

        # Output preview JSON
        print(json.dumps({
            "dry_run": True,
            "skill_name": skill_data["name"],
            "version": skill_data.get("version", "1.0"),
            "team": skill_data["team"],
            "bundle_files": file_count,
            "bundle_size": bundle_size
        }, indent=2))
        sys.exit(0)

    print()

    # Step 1: Create upload object
    print("[1/3] Creating upload object...", file=sys.stderr)
    upload_info = create_file_upload(api_key, file_name, "application/json")

    if not upload_info:
        sys.exit(1)

    file_upload_id = upload_info["id"]
    upload_url = upload_info["upload_url"]
    print(f"[OK] Upload ID: {file_upload_id[:8]}...", file=sys.stderr)

    # Step 2: Upload bundle
    print("[2/3] Uploading bundle...", file=sys.stderr)
    success = upload_file_content(api_key, upload_url, file_name, bundle_json, "application/json")

    if not success:
        sys.exit(1)

    print("[OK] Bundle uploaded", file=sys.stderr)

    # Step 3: Create page
    print("[3/3] Creating database entry...", file=sys.stderr)
    page = create_database_entry(api_key, database_id, skill_data, file_upload_id, file_name, user_id)

    if not page:
        sys.exit(1)

    page_url = page.get("url")
    print(f"\n[SUCCESS] Skill uploaded to Notion!", file=sys.stderr)
    print(f"[SUCCESS] URL: {page_url}", file=sys.stderr)
    print(f"[SUCCESS] Files in bundle: {file_count}", file=sys.stderr)

    # Output JSON for programmatic use
    print(json.dumps({
        "page_id": page.get("id"),
        "url": page_url,
        "skill_name": skill_data["name"],
        "version": skill_data.get("version", "1.0"),
        "bundle_files": file_count
    }, indent=2))

    sys.exit(0)


if __name__ == "__main__":
    main()
