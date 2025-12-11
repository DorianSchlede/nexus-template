#!/usr/bin/env python3
"""
Download Skill from Notion - Downloads skill bundle from Notion database entry

Supports multiple formats:
- JSON bundles (.skill.json) - Preferred format with all skill files
- ZIP archives (.zip) - Legacy format
- Single files (.txt, .md) - Simple skills

Supports batch import with multiple page IDs.

Usage:
    python download_skill.py <page_id> [--output-dir DIR]
    python download_skill.py <page_id1> <page_id2> ... (batch import)
    python download_skill.py <page_id> --no-backup

Examples:
    python download_skill.py abc123-page-id
    python download_skill.py abc123 def456 ghi789  # batch import
    python download_skill.py abc123-page-id --output-dir 03-skills
    python download_skill.py abc123-page-id --no-backup

Returns:
    Exit code 0 if successful, 1 if error
"""

import sys
import os
import json
import argparse
import base64
import zipfile
import io
import shutil
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    print("[ERROR] requests library not installed")
    print("Install with: pip install requests")
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


def backup_existing_skill(skill_path, backup_dir):
    """
    Backup existing skill folder before overwriting

    Args:
        skill_path: Path to existing skill folder
        backup_dir: Directory for backups (e.g., 03-skills/.backup/)

    Returns:
        Path to backup or None if no backup needed
    """
    if not skill_path.exists():
        return None

    # Create backup directory
    backup_dir = Path(backup_dir)
    backup_dir.mkdir(parents=True, exist_ok=True)

    # Create timestamped backup name
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    skill_name = skill_path.name
    backup_name = f"{skill_name}_{timestamp}"
    backup_path = backup_dir / backup_name

    # Copy skill to backup
    shutil.copytree(skill_path, backup_path)

    return backup_path


def get_page_properties(api_key, page_id):
    """
    Get Notion page properties

    Returns:
        Dict with page metadata or None if error
    """
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"[ERROR] Page not found: {page_id}", file=sys.stderr)
            return None
        elif response.status_code == 401:
            print("[ERROR] Unauthorized - invalid API key", file=sys.stderr)
            return None
        else:
            print(f"[ERROR] Failed to get page: {response.status_code}", file=sys.stderr)
            print(f"Response: {response.text}", file=sys.stderr)
            return None

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}", file=sys.stderr)
        return None


def extract_file_url(page_data):
    """
    Extract file URL from Notion page properties

    Returns:
        Tuple of (file_url, file_name) or (None, None) if no file
    """
    props = page_data.get("properties", {})
    skill_prop = props.get("Skill", {})

    files = skill_prop.get("files", [])
    if not files:
        return None, None

    # Get first file
    file_obj = files[0]
    file_type = file_obj.get("type")

    if file_type == "external":
        url = file_obj.get("external", {}).get("url")
    elif file_type == "file":
        url = file_obj.get("file", {}).get("url")
    else:
        return None, None

    name = file_obj.get("name", "skill-file.txt")

    return url, name


def download_file_content(url):
    """
    Download file from URL and return content

    Returns:
        Bytes content or None if error
    """
    try:
        response = requests.get(url, timeout=60)

        if response.status_code == 200:
            return response.content
        else:
            print(f"[ERROR] Download failed: {response.status_code}", file=sys.stderr)
            return None

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Download failed: {e}", file=sys.stderr)
        return None


def extract_json_bundle(content, output_dir, backup_dir=None):
    """
    Extract JSON bundle to skill folder

    Args:
        content: JSON bundle as bytes
        output_dir: Directory to extract to (parent of skill folder)
        backup_dir: Directory for backups (optional)

    Returns:
        Tuple of (skill_path, file_count, backup_path) or (None, 0, None) on error
    """
    try:
        bundle = json.loads(content.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"[ERROR] Invalid JSON bundle: {e}", file=sys.stderr)
        return None, 0, None

    # Validate bundle format
    if bundle.get("bundle_format") != "nexus-skill-bundle-v1":
        print(f"[WARN] Unknown bundle format: {bundle.get('bundle_format')}", file=sys.stderr)
        # Continue anyway - might be compatible

    skill_name = bundle.get("skill_name")
    if not skill_name:
        print("[ERROR] Bundle missing skill_name", file=sys.stderr)
        return None, 0, None

    files = bundle.get("files", {})
    if not files:
        print("[ERROR] Bundle contains no files", file=sys.stderr)
        return None, 0, None

    # Create skill folder path
    skill_path = Path(output_dir) / skill_name

    # Backup existing if present
    backup_path = None
    if skill_path.exists() and backup_dir:
        backup_path = backup_existing_skill(skill_path, backup_dir)
        if backup_path:
            print(f"[BACKUP] Existing skill backed up to: {backup_path.name}", file=sys.stderr)

    # Remove existing
    if skill_path.exists():
        shutil.rmtree(skill_path)

    skill_path.mkdir(parents=True)

    # Extract files
    file_count = 0
    for rel_path, content_b64 in files.items():
        try:
            content = base64.b64decode(content_b64)
            file_path = skill_path / rel_path

            # Create parent directories
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            file_path.write_bytes(content)
            file_count += 1
            print(f"  ✓ {rel_path}", file=sys.stderr)

        except Exception as e:
            print(f"  ✗ {rel_path}: {e}", file=sys.stderr)

    return skill_path, file_count, backup_path


def extract_zip_archive(content, output_dir, backup_dir=None):
    """
    Extract ZIP archive to skill folder

    Returns:
        Tuple of (skill_path, file_count, backup_path) or (None, 0, None) on error
    """
    try:
        # Extract to temp location first
        temp_dir = Path(output_dir) / '_temp_extract'
        temp_dir.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(io.BytesIO(content)) as z:
            z.extractall(temp_dir)

        # Find extracted folder (filter out mac files)
        extracted_items = [x for x in temp_dir.iterdir()
                         if not x.name.startswith('._') and not x.name.startswith('__MACOSX')]

        if not extracted_items:
            print("[ERROR] ZIP archive is empty", file=sys.stderr)
            shutil.rmtree(temp_dir)
            return None, 0, None

        # Move to final location
        source = extracted_items[0]
        backup_path = None

        if source.is_dir():
            skill_name = source.name
            skill_path = Path(output_dir) / skill_name

            # Backup existing
            if skill_path.exists() and backup_dir:
                backup_path = backup_existing_skill(skill_path, backup_dir)
                if backup_path:
                    print(f"[BACKUP] Existing skill backed up to: {backup_path.name}", file=sys.stderr)

            if skill_path.exists():
                shutil.rmtree(skill_path)

            shutil.move(str(source), str(skill_path))
        else:
            # Single file - need to determine skill name
            skill_name = source.stem.replace('.skill', '').replace('-SKILL', '')
            skill_path = Path(output_dir) / skill_name

            # Backup existing
            if skill_path.exists() and backup_dir:
                backup_path = backup_existing_skill(skill_path, backup_dir)
                if backup_path:
                    print(f"[BACKUP] Existing skill backed up to: {backup_path.name}", file=sys.stderr)

            if skill_path.exists():
                shutil.rmtree(skill_path)

            skill_path.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(skill_path / 'SKILL.md'))

        # Cleanup
        shutil.rmtree(temp_dir)

        # Clean mac files
        for root, dirs, files in os.walk(skill_path):
            for f in files:
                if f.startswith('._') or f == '.DS_Store':
                    os.remove(os.path.join(root, f))

        # Count files
        file_count = sum(1 for _ in skill_path.rglob('*') if _.is_file())

        return skill_path, file_count, backup_path

    except zipfile.BadZipFile:
        print("[ERROR] Invalid ZIP archive", file=sys.stderr)
        return None, 0, None
    except Exception as e:
        print(f"[ERROR] Failed to extract ZIP: {e}", file=sys.stderr)
        return None, 0, None


def extract_single_file(content, file_name, output_dir, backup_dir=None):
    """
    Extract single file (txt/md) to skill folder

    Returns:
        Tuple of (skill_path, file_count, backup_path) or (None, 0, None) on error
    """
    # Determine skill name from filename
    skill_name = file_name.replace('.skill.json', '').replace('.txt', '').replace('.md', '').replace('-SKILL', '')

    skill_path = Path(output_dir) / skill_name

    # Backup existing
    backup_path = None
    if skill_path.exists() and backup_dir:
        backup_path = backup_existing_skill(skill_path, backup_dir)
        if backup_path:
            print(f"[BACKUP] Existing skill backed up to: {backup_path.name}", file=sys.stderr)

    if skill_path.exists():
        shutil.rmtree(skill_path)

    skill_path.mkdir(parents=True)

    # Save as SKILL.md
    skill_file = skill_path / 'SKILL.md'
    skill_file.write_bytes(content)

    return skill_path, 1, backup_path


def extract_skill_metadata(page_data):
    """Extract skill metadata from Notion page"""
    props = page_data.get("properties", {})

    def get_text(prop):
        if not prop:
            return ""
        prop_type = prop.get("type")
        if prop_type == "title":
            return " ".join([t.get("plain_text", "") for t in prop.get("title", [])])
        elif prop_type == "rich_text":
            return " ".join([t.get("plain_text", "") for t in prop.get("rich_text", [])])
        return ""

    def get_select(prop):
        if not prop:
            return None
        select = prop.get("select")
        return select.get("name") if select else None

    return {
        "skill_name": get_text(props.get("Skill Name")),
        "description": get_text(props.get("Description")),
        "purpose": get_text(props.get("Purpose")),
        "version": get_text(props.get("Version")) or "1.0",
        "team": get_select(props.get("Team")),
        "url": page_data.get("url")
    }


def download_single_skill(api_key, page_id, output_dir, backup_dir, output_json=False):
    """
    Download a single skill from Notion

    Returns:
        Dict with result or None on error
    """
    # Get page data
    print(f"[INFO] Fetching page: {page_id}", file=sys.stderr)
    page_data = get_page_properties(api_key, page_id)

    if not page_data:
        return None

    # Extract metadata
    metadata = extract_skill_metadata(page_data)
    print(f"[INFO] Skill: {metadata['skill_name']} (v{metadata['version']})", file=sys.stderr)

    # Extract file URL
    file_url, file_name = extract_file_url(page_data)

    if not file_url:
        print("[ERROR] No file attached to this page", file=sys.stderr)
        print("[HINT] Check the 'Skill' property has a file attachment", file=sys.stderr)
        return None

    print(f"[INFO] Downloading: {file_name}", file=sys.stderr)

    # Download file content
    content = download_file_content(file_url)

    if not content:
        return None

    print(f"[OK] Downloaded: {len(content):,} bytes", file=sys.stderr)

    # Detect file type and extract accordingly
    print(f"[INFO] Extracting skill...", file=sys.stderr)

    if file_name.endswith('.skill.json') or file_name.endswith('.json'):
        # JSON bundle format (preferred)
        skill_path, file_count, backup_path = extract_json_bundle(content, output_dir, backup_dir)
    elif file_name.endswith('.zip'):
        # ZIP archive (legacy)
        skill_path, file_count, backup_path = extract_zip_archive(content, output_dir, backup_dir)
    else:
        # Single file (txt/md)
        skill_path, file_count, backup_path = extract_single_file(content, file_name, output_dir, backup_dir)

    if not skill_path:
        return None

    print(f"\n[SUCCESS] Skill extracted to: {skill_path}", file=sys.stderr)
    print(f"[SUCCESS] Files: {file_count}", file=sys.stderr)

    result = {
        "skill_name": metadata['skill_name'],
        "version": metadata['version'],
        "skill_path": str(skill_path),
        "files_extracted": file_count,
        "source_url": metadata['url'],
        "backup_path": str(backup_path) if backup_path else None
    }

    if not output_json:
        # Show extracted structure
        print(f"\nSkill structure:", file=sys.stderr)
        for f in sorted(skill_path.rglob('*')):
            if f.is_file():
                rel = f.relative_to(skill_path)
                print(f"  {rel}", file=sys.stderr)

    return result


def main():
    """Main entry point"""
    # Configure UTF-8 output
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(
        description="Download skill(s) from Notion and extract to skill folder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  python download_skill.py abc123-page-id
  python download_skill.py abc123 def456 ghi789  # batch import
  python download_skill.py abc123-page-id --output-dir 03-skills
  python download_skill.py abc123-page-id --no-backup
        """
    )
    parser.add_argument("page_ids", nargs='+', help="One or more Notion page IDs")
    parser.add_argument("--output-dir", help="Output directory for skill folder (default: 03-skills)")
    parser.add_argument("--no-backup", action="store_true", help="Don't backup existing skills before overwriting")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")

    args = parser.parse_args()

    # Find Nexus root and load config
    root = find_nexus_root()
    env_path = root / '.env'
    env_vars = load_env_file(env_path)

    # Get API key
    api_key = env_vars.get('NOTION_API_KEY') or os.getenv('NOTION_API_KEY')

    if not api_key:
        print("[ERROR] NOTION_API_KEY not found in .env or environment", file=sys.stderr)
        sys.exit(1)

    # Determine output directory
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = root / '03-skills'

    output_dir.mkdir(parents=True, exist_ok=True)

    # Determine backup directory
    backup_dir = None if args.no_backup else (output_dir / '.backup')

    # Process page IDs
    results = []
    errors = []

    is_batch = len(args.page_ids) > 1

    if is_batch:
        print(f"\n{'='*50}", file=sys.stderr)
        print(f"[BATCH] Importing {len(args.page_ids)} skills", file=sys.stderr)
        print(f"{'='*50}\n", file=sys.stderr)

    for i, page_id in enumerate(args.page_ids, 1):
        if is_batch:
            print(f"\n[{i}/{len(args.page_ids)}] Processing...", file=sys.stderr)
            print("-" * 40, file=sys.stderr)

        result = download_single_skill(api_key, page_id, output_dir, backup_dir, output_json=args.json)

        if result:
            results.append(result)
        else:
            errors.append(page_id)

    # Summary for batch
    if is_batch:
        print(f"\n{'='*50}", file=sys.stderr)
        print(f"[BATCH COMPLETE]", file=sys.stderr)
        print(f"  ✓ Success: {len(results)}", file=sys.stderr)
        if errors:
            print(f"  ✗ Failed: {len(errors)}", file=sys.stderr)
            for err in errors:
                print(f"    - {err}", file=sys.stderr)
        print(f"{'='*50}", file=sys.stderr)

    # Output JSON
    if args.json:
        if is_batch:
            print(json.dumps({
                "batch": True,
                "total": len(args.page_ids),
                "success": len(results),
                "failed": len(errors),
                "results": results,
                "errors": errors
            }, indent=2))
        elif results:
            print(json.dumps(results[0], indent=2))

    # Exit code
    if errors and not results:
        sys.exit(1)  # All failed
    elif errors:
        sys.exit(2)  # Partial success
    else:
        sys.exit(0)  # All success


if __name__ == "__main__":
    main()
