#!/usr/bin/env python3
"""
Manage Notion Databases - Create new databases and update schemas

Usage:
    python manage_database.py create --parent <page_id> --title "Database Name" --properties '...'
    python manage_database.py update --db <database_id> --add-property '...'
    python manage_database.py update --db <database_id> --update-property '...'

Examples:
    # Create a simple database
    python manage_database.py create --parent abc123 --title "Tasks" --properties '[{"name": "Status", "type": "select", "options": ["Todo", "In Progress", "Done"]}]'

    # Add a property to existing database
    python manage_database.py update --db def456 --add-property '{"name": "Priority", "type": "select", "options": ["Low", "Medium", "High"]}'

    # Update property options
    python manage_database.py update --db def456 --update-property '{"name": "Status", "options": ["Backlog", "Todo", "In Progress", "Done"]}'

Returns:
    Exit code 0 on success, 1 on error
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


def build_property_schema(prop_def):
    """
    Build Notion property schema from simplified definition

    Args:
        prop_def: Dict with name, type, and type-specific options

    Returns:
        Dict with Notion API property schema
    """
    prop_type = prop_def.get('type', 'rich_text')
    schema = {}

    if prop_type == 'title':
        schema = {"title": {}}

    elif prop_type == 'rich_text':
        schema = {"rich_text": {}}

    elif prop_type == 'number':
        schema = {"number": {"format": prop_def.get('format', 'number')}}

    elif prop_type == 'select':
        options = prop_def.get('options', [])
        schema = {
            "select": {
                "options": [{"name": opt} for opt in options]
            }
        }

    elif prop_type == 'multi_select':
        options = prop_def.get('options', [])
        schema = {
            "multi_select": {
                "options": [{"name": opt} for opt in options]
            }
        }

    elif prop_type == 'status':
        options = prop_def.get('options', ['Not Started', 'In Progress', 'Done'])
        schema = {
            "status": {
                "options": [{"name": opt} for opt in options]
            }
        }

    elif prop_type == 'date':
        schema = {"date": {}}

    elif prop_type == 'people':
        schema = {"people": {}}

    elif prop_type == 'files':
        schema = {"files": {}}

    elif prop_type == 'checkbox':
        schema = {"checkbox": {}}

    elif prop_type == 'url':
        schema = {"url": {}}

    elif prop_type == 'email':
        schema = {"email": {}}

    elif prop_type == 'phone_number':
        schema = {"phone_number": {}}

    elif prop_type == 'relation':
        schema = {
            "relation": {
                "database_id": prop_def.get('database_id'),
                "single_property": {}
            }
        }

    elif prop_type == 'rollup':
        schema = {
            "rollup": {
                "relation_property_name": prop_def.get('relation_property'),
                "rollup_property_name": prop_def.get('rollup_property'),
                "function": prop_def.get('function', 'count')
            }
        }

    elif prop_type == 'formula':
        schema = {
            "formula": {
                "expression": prop_def.get('expression', '')
            }
        }

    else:
        print(f"[WARN] Unknown property type: {prop_type}", file=sys.stderr)
        schema = {"rich_text": {}}

    return schema


def create_database(api_key, parent_id, title, properties, is_inline=False):
    """
    Create a new Notion database

    Args:
        api_key: Notion API key
        parent_id: Parent page ID
        title: Database title
        properties: List of property definitions
        is_inline: Whether to create inline database

    Returns:
        Created database object or None on error
    """
    url = "https://api.notion.com/v1/databases"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    # Build properties schema
    props_schema = {}

    # Title property is required
    has_title = any(p.get('type') == 'title' for p in properties)
    if not has_title:
        props_schema["Name"] = {"title": {}}

    for prop in properties:
        name = prop.get('name', 'Untitled')
        props_schema[name] = build_property_schema(prop)

    body = {
        "parent": {"type": "page_id", "page_id": parent_id},
        "title": [{"type": "text", "text": {"content": title}}],
        "properties": props_schema,
        "is_inline": is_inline
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
            print(f"[ERROR] 404 Not Found - Parent page not accessible: {parent_id}", file=sys.stderr)
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


def update_database(api_key, database_id, updates):
    """
    Update an existing Notion database

    Args:
        api_key: Notion API key
        database_id: Database ID to update
        updates: Dict with updates (title, properties, etc.)

    Returns:
        Updated database object or None on error
    """
    url = f"https://api.notion.com/v1/databases/{database_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    try:
        response = requests.patch(url, headers=headers, json=updates, timeout=30)

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
            print(f"[ERROR] 404 Not Found - Database not accessible: {database_id}", file=sys.stderr)
            return None
        else:
            print(f"[ERROR] Update failed: {response.status_code}", file=sys.stderr)
            print(f"Response: {response.text}", file=sys.stderr)
            return None

    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}", file=sys.stderr)
        return None


def get_database(api_key, database_id):
    """Get current database schema"""
    url = f"https://api.notion.com/v1/databases/{database_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None


def update_context_file(root_path, database):
    """Update context file with new/updated database"""
    context_file = root_path / "01-memory" / "integrations" / "notion-databases.yaml"

    if not context_file.exists():
        print("[INFO] Context file not found, run discover_databases.py to create", file=sys.stderr)
        return

    try:
        with open(context_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse YAML frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 2:
                context = yaml.safe_load(parts[1])
            else:
                context = {}
        else:
            context = yaml.safe_load(content) or {}

        # Find or add database entry
        databases = context.get('databases', [])
        db_id = database.get('id')

        found = False
        for i, db in enumerate(databases):
            if db.get('id') == db_id:
                # Update existing entry
                databases[i] = format_database_for_context(database)
                found = True
                break

        if not found:
            # Add new entry
            databases.append(format_database_for_context(database))

        context['databases'] = databases
        context['last_synced'] = datetime.now().isoformat()
        context['database_count'] = len(databases)

        # Write back
        with open(context_file, 'w', encoding='utf-8') as f:
            f.write("---\n")
            yaml.dump(context, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            f.write("---\n\n")
            f.write("# Notion Databases Context\n\n")
            f.write("Auto-generated by notion-connect skill.\n")
            f.write("Run \"refresh notion\" to update.\n")

        print(f"[INFO] Updated context file with database: {database.get('id')}", file=sys.stderr)

    except Exception as e:
        print(f"[WARN] Failed to update context file: {e}", file=sys.stderr)


def format_database_for_context(db):
    """Format database for context file"""
    title_array = db.get("title", [])
    name = " ".join([t.get("plain_text", "") for t in title_array]) if title_array else "Untitled"

    properties = []
    for prop_name, prop_config in db.get("properties", {}).items():
        prop_type = prop_config.get("type")
        prop_entry = {"name": prop_name, "type": prop_type}

        # Extract options for select types
        if prop_type == "select":
            options = prop_config.get("select", {}).get("options", [])
            prop_entry["options"] = [opt.get("name") for opt in options]
        elif prop_type == "multi_select":
            options = prop_config.get("multi_select", {}).get("options", [])
            prop_entry["options"] = [opt.get("name") for opt in options]
        elif prop_type == "status":
            options = prop_config.get("status", {}).get("options", [])
            prop_entry["options"] = [opt.get("name") for opt in options]

        properties.append(prop_entry)

    # Sort: title first, then alphabetically
    properties.sort(key=lambda p: (p["type"] != "title", p["name"].lower()))

    return {
        "id": db.get("id"),
        "name": name,
        "parent": None,
        "url": db.get("url"),
        "created": db.get("created_time"),
        "last_edited": db.get("last_edited_time"),
        "properties": properties
    }


def main():
    """Main entry point"""
    # Configure UTF-8 output
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(
        description="Create and manage Notion databases",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new database')
    create_parser.add_argument('--parent', required=True, help='Parent page ID')
    create_parser.add_argument('--title', required=True, help='Database title')
    create_parser.add_argument('--properties', default='[]', help='JSON array of property definitions')
    create_parser.add_argument('--inline', action='store_true', help='Create as inline database')
    create_parser.add_argument('--json', action='store_true', help='Output raw JSON')

    # Update command
    update_parser = subparsers.add_parser('update', help='Update an existing database')
    update_parser.add_argument('--db', required=True, help='Database ID to update')
    update_parser.add_argument('--title', help='New database title')
    update_parser.add_argument('--add-property', help='JSON property definition to add')
    update_parser.add_argument('--update-property', help='JSON property definition to update')
    update_parser.add_argument('--json', action='store_true', help='Output raw JSON')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
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

    if args.command == 'create':
        # Parse properties
        try:
            properties = json.loads(args.properties)
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid JSON for properties: {e}", file=sys.stderr)
            sys.exit(1)

        print(f"[INFO] Creating database: {args.title}", file=sys.stderr)
        result = create_database(api_key, args.parent, args.title, properties, args.inline)

        if result:
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"\n✅ Database created successfully!")
                print(f"   ID: {result.get('id')}")
                print(f"   URL: {result.get('url')}")
                print(f"   Properties: {len(result.get('properties', {}))}")

            # Update context file
            update_context_file(root, result)
            sys.exit(0)
        else:
            sys.exit(1)

    elif args.command == 'update':
        updates = {"properties": {}}

        # Get current database schema
        current = get_database(api_key, args.db)
        if not current:
            print(f"[ERROR] Could not retrieve database: {args.db}", file=sys.stderr)
            sys.exit(1)

        # Update title if provided
        if args.title:
            updates["title"] = [{"type": "text", "text": {"content": args.title}}]

        # Add new property
        if args.add_property:
            try:
                prop_def = json.loads(args.add_property)
                name = prop_def.get('name', 'New Property')
                updates["properties"][name] = build_property_schema(prop_def)
                print(f"[INFO] Adding property: {name}", file=sys.stderr)
            except json.JSONDecodeError as e:
                print(f"[ERROR] Invalid JSON for add-property: {e}", file=sys.stderr)
                sys.exit(1)

        # Update existing property
        if args.update_property:
            try:
                prop_def = json.loads(args.update_property)
                name = prop_def.get('name')
                if not name:
                    print("[ERROR] Property name required for update", file=sys.stderr)
                    sys.exit(1)

                # Check property exists
                if name not in current.get('properties', {}):
                    print(f"[ERROR] Property '{name}' not found in database", file=sys.stderr)
                    sys.exit(1)

                updates["properties"][name] = build_property_schema(prop_def)
                print(f"[INFO] Updating property: {name}", file=sys.stderr)
            except json.JSONDecodeError as e:
                print(f"[ERROR] Invalid JSON for update-property: {e}", file=sys.stderr)
                sys.exit(1)

        # Remove empty properties dict if no property changes
        if not updates["properties"]:
            del updates["properties"]

        if not updates:
            print("[WARN] No updates specified", file=sys.stderr)
            sys.exit(0)

        result = update_database(api_key, args.db, updates)

        if result:
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"\n✅ Database updated successfully!")
                print(f"   ID: {result.get('id')}")
                print(f"   URL: {result.get('url')}")

            # Update context file
            update_context_file(root, result)
            sys.exit(0)
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
