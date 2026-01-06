#!/usr/bin/env python3
"""
Create Notion Page - Create pages in any database with property validation

Usage:
    python create_page.py --db <database_name_or_id> --properties '{"Title": "...", "Status": "..."}'
    python create_page.py --db <database_name_or_id> --interactive

Examples:
    python create_page.py --db "Tasks" --properties '{"Name": "New Task", "Status": "Todo", "Priority": "High"}'
    python create_page.py --db "Projects" --interactive
    python create_page.py --db abc123-def456 --properties '{"Title": "Test"}'

Returns:
    Exit code 0 on success, 1 on error, 2 if database not found
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    print("[ERROR] requests library not installed", file=sys.stderr)
    print("Install with: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    import yaml
except ImportError:
    print("[ERROR] PyYAML library not installed", file=sys.stderr)
    print("Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def find_nexus_root():
    """Find Nexus root directory (contains CLAUDE.md)"""
    current = Path.cwd()
    for path in [current] + list(current.parents):
        if (path / 'CLAUDE.md').exists():
            return path
    return current


def load_env_file(env_path):
    """Load .env file and return as dict"""
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


def load_context_file(root_path):
    """Load notion-databases.yaml context file"""
    context_file = root_path / "01-memory" / "integrations" / "notion-databases.yaml"

    if not context_file.exists():
        return None

    try:
        with open(context_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 2:
                return yaml.safe_load(parts[1])

        return yaml.safe_load(content)

    except Exception as e:
        print(f"[ERROR] Failed to load context file: {e}", file=sys.stderr)
        return None


def find_database(name_or_id, context):
    """Find database by name (fuzzy) or ID (exact)"""
    import re

    if not context or 'databases' not in context:
        return None, []

    databases = context['databases']
    search = name_or_id.lower().strip()

    # Check if UUID
    uuid_pattern = r'^[a-f0-9]{8}-?[a-f0-9]{4}-?[a-f0-9]{4}-?[a-f0-9]{4}-?[a-f0-9]{12}$'
    if re.match(uuid_pattern, search.replace('-', '')):
        normalized_id = search.replace('-', '')
        for db in databases:
            if db['id'].replace('-', '') == normalized_id:
                return db, []
        return None, []

    # Search by name
    exact_matches = []
    partial_matches = []

    for db in databases:
        db_name = db['name'].lower()
        if db_name == search:
            exact_matches.append(db)
        elif search in db_name:
            partial_matches.append(db)

    all_matches = exact_matches + partial_matches
    if len(all_matches) == 1:
        return all_matches[0], []
    elif len(all_matches) > 1:
        return None, all_matches

    return None, []


def build_property_value(prop_schema, value):
    """
    Build Notion property value from user input

    Args:
        prop_schema: Property schema from context file
        value: User-provided value

    Returns:
        Notion API property value or None if invalid
    """
    prop_type = prop_schema.get('type')

    if prop_type == 'title':
        return {"title": [{"text": {"content": str(value)}}]}

    elif prop_type == 'rich_text':
        return {"rich_text": [{"text": {"content": str(value)}}]}

    elif prop_type == 'number':
        try:
            return {"number": float(value)}
        except ValueError:
            print(f"[WARN] Invalid number: {value}", file=sys.stderr)
            return None

    elif prop_type == 'select':
        options = prop_schema.get('options', [])
        if options and value not in options:
            print(f"[WARN] Invalid option '{value}'. Valid: {options}", file=sys.stderr)
            return None
        return {"select": {"name": str(value)}}

    elif prop_type == 'multi_select':
        if isinstance(value, str):
            values = [v.strip() for v in value.split(',')]
        else:
            values = value
        options = prop_schema.get('options', [])
        if options:
            invalid = [v for v in values if v not in options]
            if invalid:
                print(f"[WARN] Invalid options: {invalid}. Valid: {options}", file=sys.stderr)
        return {"multi_select": [{"name": v} for v in values]}

    elif prop_type == 'status':
        options = prop_schema.get('options', [])
        if options and value not in options:
            print(f"[WARN] Invalid status '{value}'. Valid: {options}", file=sys.stderr)
            return None
        return {"status": {"name": str(value)}}

    elif prop_type == 'date':
        # Accept YYYY-MM-DD or ISO format
        return {"date": {"start": str(value)}}

    elif prop_type == 'checkbox':
        bool_val = str(value).lower() in ['true', 'yes', '1', 'checked']
        return {"checkbox": bool_val}

    elif prop_type == 'url':
        return {"url": str(value)}

    elif prop_type == 'email':
        return {"email": str(value)}

    elif prop_type == 'phone_number':
        return {"phone_number": str(value)}

    elif prop_type == 'people':
        # Expect user IDs
        if isinstance(value, str):
            user_ids = [v.strip() for v in value.split(',')]
        else:
            user_ids = value
        return {"people": [{"id": uid} for uid in user_ids]}

    elif prop_type == 'relation':
        # Expect page IDs
        if isinstance(value, str):
            page_ids = [v.strip() for v in value.split(',')]
        else:
            page_ids = value
        return {"relation": [{"id": pid} for pid in page_ids]}

    elif prop_type == 'files':
        # Files must be created separately
        print(f"[WARN] File properties cannot be set directly", file=sys.stderr)
        return None

    else:
        print(f"[WARN] Unknown property type: {prop_type}", file=sys.stderr)
        return None


def create_page(api_key, database_id, properties):
    """
    Create a new page in a Notion database

    Args:
        api_key: Notion API key
        database_id: Target database ID
        properties: Dict of property values in Notion API format

    Returns:
        Created page object or None on error
    """
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    body = {
        "parent": {"type": "database_id", "database_id": database_id},
        "properties": properties
    }

    try:
        response = requests.post(url, headers=headers, json=body, timeout=30)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            error = response.json()
            print(f"[ERROR] Bad request: {error.get('message', 'Unknown error')}", file=sys.stderr)
            return None
        elif response.status_code == 401:
            print("[ERROR] 401 Unauthorized - Invalid API key", file=sys.stderr)
            return None
        elif response.status_code == 404:
            print(f"[ERROR] 404 Not Found - Database not accessible", file=sys.stderr)
            return None
        else:
            print(f"[ERROR] Create failed: {response.status_code}", file=sys.stderr)
            print(f"Response: {response.text}", file=sys.stderr)
            return None

    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}", file=sys.stderr)
        return None


def interactive_mode(db_schema):
    """Prompt user for property values interactively"""
    properties = {}

    print("\nEnter property values (press Enter to skip optional fields):\n")

    for prop in db_schema.get('properties', []):
        name = prop['name']
        prop_type = prop['type']
        options = prop.get('options', [])

        # Build prompt
        prompt = f"  {name}"
        if prop_type in ['select', 'multi_select', 'status'] and options:
            prompt += f" [{'/'.join(options[:5])}"
            if len(options) > 5:
                prompt += "/..."
            prompt += "]"
        elif prop_type == 'date':
            prompt += " [YYYY-MM-DD]"
        elif prop_type == 'checkbox':
            prompt += " [yes/no]"
        elif prop_type == 'multi_select':
            prompt += " [comma-separated]"

        if prop_type == 'title':
            prompt += " (required)"

        prompt += ": "

        # Get input
        value = input(prompt).strip()

        if value:
            properties[name] = value
        elif prop_type == 'title':
            print("  [ERROR] Title is required")
            return None

    return properties


def main():
    """Main entry point"""
    # Configure UTF-8 output
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(
        description="Create pages in any Notion database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python create_page.py --db "Tasks" --properties '{"Name": "New Task", "Status": "Todo"}'
  python create_page.py --db "Projects" --interactive
        """
    )
    parser.add_argument("--db", required=True, help="Database name or ID")
    parser.add_argument("--properties", help="JSON object with property values")
    parser.add_argument("--interactive", action="store_true", help="Prompt for each property")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    if not args.properties and not args.interactive:
        print("[ERROR] Either --properties or --interactive is required", file=sys.stderr)
        sys.exit(1)

    # Find Nexus root and load config
    root = find_nexus_root()
    env_path = root / '.env'
    env_vars = load_env_file(env_path)

    # Get API key
    api_key = env_vars.get('NOTION_API_KEY') or os.getenv('NOTION_API_KEY')

    if not api_key:
        print("[ERROR] NOTION_API_KEY not found", file=sys.stderr)
        sys.exit(1)

    # Load context
    context = load_context_file(root)
    if not context:
        print("[ERROR] No database context found", file=sys.stderr)
        print("[HINT] Run: python discover_databases.py", file=sys.stderr)
        sys.exit(2)

    # Find database
    db, matches = find_database(args.db, context)

    if not db and matches:
        print(f"[INFO] Found {len(matches)} matching databases:", file=sys.stderr)
        for i, m in enumerate(matches, 1):
            print(f"  {i}. {m['name']}", file=sys.stderr)
        print("\nPlease be more specific.", file=sys.stderr)
        sys.exit(2)

    if not db:
        print(f"[ERROR] Database '{args.db}' not found", file=sys.stderr)
        print("[HINT] Run: python discover_databases.py --refresh", file=sys.stderr)
        sys.exit(2)

    print(f"[INFO] Creating page in: {db['name']}", file=sys.stderr)

    # Get property values
    if args.interactive:
        user_props = interactive_mode(db)
        if user_props is None:
            sys.exit(1)
    else:
        try:
            user_props = json.loads(args.properties)
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid JSON: {e}", file=sys.stderr)
            sys.exit(1)

    # Build Notion API properties
    api_props = {}
    schema_map = {p['name'].lower(): p for p in db.get('properties', [])}

    for name, value in user_props.items():
        # Find matching schema (case-insensitive)
        schema = schema_map.get(name.lower())
        if not schema:
            print(f"[WARN] Property '{name}' not found in schema, skipping", file=sys.stderr)
            continue

        # Use exact case from schema
        prop_name = schema['name']
        prop_value = build_property_value(schema, value)

        if prop_value:
            api_props[prop_name] = prop_value

    if not api_props:
        print("[ERROR] No valid properties to create page", file=sys.stderr)
        sys.exit(1)

    # Create page
    result = create_page(api_key, db['id'], api_props)

    if result:
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"\n✅ Page created successfully!")
            print(f"   ID: {result.get('id')}")
            print(f"   URL: {result.get('url')}")

        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
