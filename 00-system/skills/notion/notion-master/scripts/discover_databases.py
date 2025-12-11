#!/usr/bin/env python3
"""
Discover Notion Databases - Find all accessible databases and cache schemas

Usage:
    python discover_databases.py [--refresh] [--json]

Examples:
    python discover_databases.py           # Discover and save to context file
    python discover_databases.py --refresh # Force refresh even if context exists
    python discover_databases.py --json    # Output JSON only (no file save)

Returns:
    Exit code 0 on success, 1 on error
    Creates/updates: 01-memory/integrations/notion-databases.yaml
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


def search_databases(api_key):
    """
    Search for all accessible databases using Notion Search API

    Args:
        api_key: Notion API key

    Returns:
        List of database objects or None on error
    """
    url = "https://api.notion.com/v1/search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    body = {
        "filter": {"property": "object", "value": "database"},
        "page_size": 100
    }

    all_databases = []
    has_more = True
    start_cursor = None

    while has_more:
        if start_cursor:
            body["start_cursor"] = start_cursor

        try:
            response = requests.post(url, headers=headers, json=body, timeout=30)

            if response.status_code == 200:
                data = response.json()
                all_databases.extend(data.get("results", []))
                has_more = data.get("has_more", False)
                start_cursor = data.get("next_cursor")
            elif response.status_code == 401:
                print("[ERROR] 401 Unauthorized - Invalid API key", file=sys.stderr)
                return None
            elif response.status_code == 429:
                print("[WARN] Rate limited - waiting 1 second...", file=sys.stderr)
                import time
                time.sleep(1)
                continue
            else:
                print(f"[ERROR] Search failed: {response.status_code}", file=sys.stderr)
                print(f"Response: {response.text}", file=sys.stderr)
                return None

        except requests.exceptions.Timeout:
            print("[ERROR] Request timed out", file=sys.stderr)
            return None
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Network error: {e}", file=sys.stderr)
            return None

    return all_databases


def get_database_schema(api_key, database_id):
    """
    Get detailed schema for a specific database

    Args:
        api_key: Notion API key
        database_id: Database ID to retrieve

    Returns:
        Database object with properties or None on error
    """
    url = f"https://api.notion.com/v1/databases/{database_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"[WARN] Database {database_id} not accessible", file=sys.stderr)
            return None
        else:
            print(f"[WARN] Failed to get schema for {database_id}: {response.status_code}", file=sys.stderr)
            return None

    except requests.exceptions.RequestException as e:
        print(f"[WARN] Error getting schema: {e}", file=sys.stderr)
        return None


def extract_property_schema(prop_name, prop_config):
    """
    Extract property schema in simplified format

    Args:
        prop_name: Property name
        prop_config: Notion property configuration

    Returns:
        Dict with property schema
    """
    prop_type = prop_config.get("type")
    schema = {
        "name": prop_name,
        "type": prop_type
    }

    # Extract options for select/multi_select
    if prop_type == "select":
        options = prop_config.get("select", {}).get("options", [])
        schema["options"] = [opt.get("name") for opt in options]
    elif prop_type == "multi_select":
        options = prop_config.get("multi_select", {}).get("options", [])
        schema["options"] = [opt.get("name") for opt in options]
    elif prop_type == "status":
        options = prop_config.get("status", {}).get("options", [])
        schema["options"] = [opt.get("name") for opt in options]
        groups = prop_config.get("status", {}).get("groups", [])
        schema["groups"] = [g.get("name") for g in groups]
    elif prop_type == "relation":
        relation = prop_config.get("relation", {})
        schema["related_database"] = relation.get("database_id")
    elif prop_type == "rollup":
        rollup = prop_config.get("rollup", {})
        schema["relation_property"] = rollup.get("relation_property_name")
        schema["rollup_property"] = rollup.get("rollup_property_name")
        schema["function"] = rollup.get("function")
    elif prop_type == "formula":
        formula = prop_config.get("formula", {})
        schema["expression"] = formula.get("expression")

    return schema


def extract_database_title(db):
    """Extract database title from Notion database object"""
    title_array = db.get("title", [])
    if title_array:
        return " ".join([t.get("plain_text", "") for t in title_array])
    return "Untitled"


def extract_parent_name(db):
    """Extract parent page/workspace name for disambiguation"""
    parent = db.get("parent", {})
    parent_type = parent.get("type")

    if parent_type == "page_id":
        # Would need another API call to get page name
        # For now, just indicate it has a parent page
        return "(Page)"
    elif parent_type == "workspace":
        return "(Workspace)"
    elif parent_type == "block_id":
        return "(Block)"

    return None


def format_database_entry(db, detailed_schema=None):
    """
    Format database info for context file

    Args:
        db: Database object from search
        detailed_schema: Optional detailed schema from get_database_schema

    Returns:
        Dict with formatted database info
    """
    # Use detailed schema if available, otherwise use search results
    source = detailed_schema or db

    entry = {
        "id": db.get("id"),
        "name": extract_database_title(source),
        "parent": extract_parent_name(db),
        "url": db.get("url"),
        "created": db.get("created_time"),
        "last_edited": db.get("last_edited_time"),
        "properties": []
    }

    # Extract property schemas
    props = source.get("properties", {})
    for prop_name, prop_config in props.items():
        prop_schema = extract_property_schema(prop_name, prop_config)
        entry["properties"].append(prop_schema)

    # Sort properties: title first, then alphabetically
    entry["properties"].sort(key=lambda p: (p["type"] != "title", p["name"].lower()))

    return entry


def save_context_file(databases, root_path):
    """
    Save databases to context file

    Args:
        databases: List of formatted database entries
        root_path: Nexus root path

    Returns:
        Path to saved file or None on error
    """
    integrations_dir = root_path / "01-memory" / "integrations"

    # Create directory if needed
    if not integrations_dir.exists():
        try:
            integrations_dir.mkdir(parents=True)
            print(f"[INFO] Created directory: {integrations_dir}", file=sys.stderr)
        except Exception as e:
            print(f"[ERROR] Failed to create directory: {e}", file=sys.stderr)
            return None

    context_file = integrations_dir / "notion-databases.yaml"

    # Load existing if present (to preserve sync_count)
    sync_count = 1
    if context_file.exists():
        try:
            with open(context_file, 'r', encoding='utf-8') as f:
                existing = yaml.safe_load(f)
                if existing and isinstance(existing, dict):
                    sync_count = existing.get("sync_count", 0) + 1
        except:
            pass

    # Build context structure
    context = {
        "last_synced": datetime.now().isoformat(),
        "sync_count": sync_count,
        "database_count": len(databases),
        "databases": databases
    }

    # Write file
    try:
        with open(context_file, 'w', encoding='utf-8') as f:
            # Write YAML frontmatter
            f.write("---\n")
            yaml.dump(context, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            f.write("---\n\n")

            # Write markdown documentation
            f.write("# Notion Databases Context\n\n")
            f.write("Auto-generated by notion-connect skill.\n")
            f.write("Run \"refresh notion\" to update.\n\n")
            f.write("## Quick Reference\n\n")

            for db in databases:
                f.write(f"### {db['name']}\n")
                f.write(f"- **ID**: `{db['id']}`\n")
                if db.get('parent'):
                    f.write(f"- **Location**: {db['parent']}\n")
                f.write(f"- **Properties**: {len(db['properties'])}\n")

                # List key properties
                key_types = ['title', 'select', 'multi_select', 'status', 'date']
                key_props = [p for p in db['properties'] if p['type'] in key_types]
                if key_props:
                    f.write("- **Key fields**: ")
                    f.write(", ".join([f"{p['name']} ({p['type']})" for p in key_props[:5]]))
                    f.write("\n")
                f.write("\n")

        return context_file

    except Exception as e:
        print(f"[ERROR] Failed to write context file: {e}", file=sys.stderr)
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
        description="Discover Notion databases and cache schemas",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--refresh", action="store_true", help="Force refresh even if context exists")
    parser.add_argument("--json", action="store_true", help="Output JSON only (no file save)")
    parser.add_argument("--detailed", action="store_true", help="Fetch full schema for each database (slower)")

    args = parser.parse_args()

    # Find Nexus root and load config
    root = find_nexus_root()
    env_path = root / '.env'
    env_vars = load_env_file(env_path)

    # Get API key
    api_key = env_vars.get('NOTION_API_KEY') or os.getenv('NOTION_API_KEY')

    if not api_key:
        print("[ERROR] NOTION_API_KEY not found in .env or environment", file=sys.stderr)
        print("Run: python 00-system/skills/notion-master/scripts/setup_notion.py", file=sys.stderr)
        sys.exit(1)

    # Check if context file exists (unless refresh requested)
    context_file = root / "01-memory" / "integrations" / "notion-databases.yaml"
    if context_file.exists() and not args.refresh and not args.json:
        print(f"[INFO] Context file exists: {context_file}", file=sys.stderr)
        print("[INFO] Use --refresh to update", file=sys.stderr)

        # Load and display current databases
        try:
            with open(context_file, 'r', encoding='utf-8') as f:
                existing = yaml.safe_load(f)
                if existing:
                    print(f"\n[INFO] Currently cached: {existing.get('database_count', 0)} databases", file=sys.stderr)
                    print(f"[INFO] Last synced: {existing.get('last_synced', 'unknown')}", file=sys.stderr)
                    for db in existing.get('databases', []):
                        print(f"  • {db['name']}", file=sys.stderr)
        except:
            pass

        sys.exit(0)

    # Search for databases
    print("[INFO] Searching for Notion databases...", file=sys.stderr)
    databases = search_databases(api_key)

    if databases is None:
        sys.exit(1)

    if not databases:
        print("[WARN] No databases found. Make sure your integration has database access.", file=sys.stderr)
        print("[HINT] In Notion, open a database → ... → Connections → Add your integration", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] Found {len(databases)} databases", file=sys.stderr)

    # Format database entries
    formatted = []
    for i, db in enumerate(databases, 1):
        name = extract_database_title(db)
        print(f"[INFO] Processing {i}/{len(databases)}: {name}", file=sys.stderr)

        # Optionally get detailed schema
        detailed = None
        if args.detailed:
            detailed = get_database_schema(api_key, db.get("id"))

        entry = format_database_entry(db, detailed)
        formatted.append(entry)

    # Sort by name
    formatted.sort(key=lambda d: d["name"].lower())

    # Output
    if args.json:
        print(json.dumps(formatted, indent=2))
    else:
        # Save to context file
        saved_path = save_context_file(formatted, root)

        if saved_path:
            print(f"\n✅ Successfully discovered {len(formatted)} databases", file=sys.stderr)
            print(f"   Saved to: {saved_path}", file=sys.stderr)
            print("\nDatabases found:", file=sys.stderr)
            for db in formatted:
                prop_count = len(db['properties'])
                print(f"  • {db['name']} ({prop_count} properties)", file=sys.stderr)
        else:
            sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
