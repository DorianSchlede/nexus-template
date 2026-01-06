#!/usr/bin/env python3
"""
DEPRECATED: Use Airtable Skill Marketplace instead.

For skill search, use:
    python 00-system/skills/airtable/airtable-master/scripts/query_records.py \
        --base app1gngDx52VAgjVQ --table tblsQL8n9EfMAFIyD --token MUTAGENT

---

Search Skill Database - Search and filter Notion skills database (LEGACY)

Usage:
    python search_skill_database.py --db <database_name_or_id> [--filter "..."] [--sort ...] [--limit N]

    # Skills DB preset mode (for Beam Nexus Skills database):
    python search_skill_database.py --skills [--team X] [--integration Y] [--name Z]

Examples:
    # General database queries:
    python search_skill_database.py --db "Projects"
    python search_skill_database.py --db "Tasks" --filter "Status = In Progress"
    python search_skill_database.py --db abc123-def456 --limit 10 --json

    # Skills DB preset (multiple filters with AND):
    python search_skill_database.py --skills --team Solutions
    python search_skill_database.py --skills --integration "Beam AI" --name notion
    python search_skill_database.py --skills --team General --integration Linear

Filter Syntax:
    --filter "Property = Value"           # Equals
    --filter "Property != Value"          # Not equals
    --filter "Property contains Value"    # Contains (text/multi_select)
    --filter "Property > Value"           # Greater than (number/date)
    --filter "Property < Value"           # Less than (number/date)
    --filter "Property is_empty"          # Is empty
    --filter "Property is_not_empty"      # Is not empty

Returns:
    Exit code 0 on success, 1 on error, 2 if database not found
"""

import sys
import os
import json
import argparse
import re
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
    """
    Load notion-databases.yaml context file

    Returns:
        Dict with databases or None if not found
    """
    context_file = root_path / "01-memory" / "integrations" / "notion-databases.yaml"

    if not context_file.exists():
        return None

    try:
        with open(context_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Handle YAML frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 2:
                yaml_content = parts[1]
                return yaml.safe_load(yaml_content)

        return yaml.safe_load(content)

    except Exception as e:
        print(f"[ERROR] Failed to load context file: {e}", file=sys.stderr)
        return None


def find_database(name_or_id, context):
    """
    Find database by name (fuzzy) or ID (exact)

    Args:
        name_or_id: Database name or ID to find
        context: Context file data

    Returns:
        (database_entry, matches_list) - single match or None with list of partial matches
    """
    if not context or 'databases' not in context:
        return None, []

    databases = context['databases']
    search = name_or_id.lower().strip()

    # Check if it's a UUID (exact match by ID)
    uuid_pattern = r'^[a-f0-9]{8}-?[a-f0-9]{4}-?[a-f0-9]{4}-?[a-f0-9]{4}-?[a-f0-9]{12}$'
    if re.match(uuid_pattern, search.replace('-', '')):
        # Search by ID
        normalized_id = search.replace('-', '')
        for db in databases:
            db_id = db['id'].replace('-', '')
            if db_id == normalized_id:
                return db, []
        return None, []

    # Search by name
    exact_matches = []
    partial_matches = []

    for db in databases:
        db_name = db['name'].lower()

        # Exact match
        if db_name == search:
            exact_matches.append(db)
        # Partial match (name contains search term)
        elif search in db_name:
            partial_matches.append(db)
        # Word match (search term is a word in the name)
        elif any(search == word.lower() for word in db['name'].split()):
            partial_matches.append(db)

    # Return single exact match
    if len(exact_matches) == 1:
        return exact_matches[0], []

    # Return multiple matches for disambiguation
    all_matches = exact_matches + partial_matches
    if len(all_matches) == 1:
        return all_matches[0], []
    elif len(all_matches) > 1:
        return None, all_matches

    return None, []


def get_property_type(db, prop_name):
    """Get property type from database schema"""
    for prop in db.get('properties', []):
        if prop['name'].lower() == prop_name.lower():
            return prop['type'], prop
    return None, None


def parse_filter_expression(filter_str, db):
    """
    Parse filter expression into Notion API filter format

    Supports:
        "Property = Value"
        "Property != Value"
        "Property contains Value"
        "Property > Value"
        "Property < Value"
        "Property is_empty"
        "Property is_not_empty"

    Returns:
        Notion API filter dict or None
    """
    if not filter_str:
        return None

    # Handle is_empty / is_not_empty
    empty_match = re.match(r'^(.+?)\s+(is_empty|is_not_empty)$', filter_str.strip(), re.IGNORECASE)
    if empty_match:
        prop_name = empty_match.group(1).strip()
        operator = empty_match.group(2).lower()

        prop_type, prop_config = get_property_type(db, prop_name)
        if not prop_type:
            print(f"[WARN] Property '{prop_name}' not found in database schema", file=sys.stderr)
            return None

        # Build filter based on property type
        filter_obj = {"property": prop_name}

        if prop_type in ['title', 'rich_text', 'url', 'email', 'phone_number']:
            filter_obj[prop_type] = {operator: True}
        elif prop_type in ['number']:
            filter_obj['number'] = {operator: True}
        elif prop_type in ['date', 'created_time', 'last_edited_time']:
            filter_obj['date'] = {operator: True}
        elif prop_type in ['select', 'status']:
            filter_obj[prop_type] = {operator: True}
        elif prop_type == 'multi_select':
            filter_obj['multi_select'] = {operator: True}
        elif prop_type == 'checkbox':
            filter_obj['checkbox'] = {operator: True}
        elif prop_type == 'people':
            filter_obj['people'] = {operator: True}
        elif prop_type == 'files':
            filter_obj['files'] = {operator: True}
        else:
            print(f"[WARN] Unsupported property type '{prop_type}' for {operator}", file=sys.stderr)
            return None

        return filter_obj

    # Handle comparison operators
    operators = [
        (r'!=', 'does_not_equal'),
        (r'>=', 'on_or_after'),  # For dates
        (r'<=', 'on_or_before'),  # For dates
        (r'>', 'greater_than'),
        (r'<', 'less_than'),
        (r'=', 'equals'),
        (r'\s+contains\s+', 'contains'),
        (r'\s+does_not_contain\s+', 'does_not_contain'),
        (r'\s+starts_with\s+', 'starts_with'),
        (r'\s+ends_with\s+', 'ends_with'),
    ]

    for pattern, api_operator in operators:
        match = re.split(pattern, filter_str.strip(), maxsplit=1, flags=re.IGNORECASE)
        if len(match) == 2:
            prop_name = match[0].strip()
            value = match[1].strip().strip('"').strip("'")

            prop_type, prop_config = get_property_type(db, prop_name)
            if not prop_type:
                print(f"[WARN] Property '{prop_name}' not found in database schema", file=sys.stderr)
                return None

            # Build filter based on property type
            filter_obj = {"property": prop_name}

            if prop_type == 'title':
                filter_obj['title'] = {api_operator: value}
            elif prop_type == 'rich_text':
                filter_obj['rich_text'] = {api_operator: value}
            elif prop_type == 'select':
                # Map operators to Notion API equivalents
                if api_operator in ['equals', 'does_not_equal']:
                    filter_obj['select'] = {api_operator: value}
                else:
                    filter_obj['select'] = {'equals': value}
            elif prop_type == 'status':
                if api_operator in ['equals', 'does_not_equal']:
                    filter_obj['status'] = {api_operator: value}
                else:
                    filter_obj['status'] = {'equals': value}
            elif prop_type == 'multi_select':
                if api_operator == 'does_not_contain':
                    filter_obj['multi_select'] = {'does_not_contain': value}
                else:
                    filter_obj['multi_select'] = {'contains': value}
            elif prop_type == 'number':
                try:
                    num_value = float(value)
                    if api_operator in ['equals', 'does_not_equal']:
                        filter_obj['number'] = {api_operator: num_value}
                    elif api_operator == 'greater_than':
                        filter_obj['number'] = {'greater_than': num_value}
                    elif api_operator == 'less_than':
                        filter_obj['number'] = {'less_than': num_value}
                except ValueError:
                    print(f"[WARN] Invalid number value: {value}", file=sys.stderr)
                    return None
            elif prop_type in ['date', 'created_time', 'last_edited_time']:
                if api_operator == 'equals':
                    filter_obj['date'] = {'equals': value}
                elif api_operator == 'greater_than':
                    filter_obj['date'] = {'after': value}
                elif api_operator == 'less_than':
                    filter_obj['date'] = {'before': value}
                elif api_operator == 'on_or_after':
                    filter_obj['date'] = {'on_or_after': value}
                elif api_operator == 'on_or_before':
                    filter_obj['date'] = {'on_or_before': value}
            elif prop_type == 'checkbox':
                filter_obj['checkbox'] = {'equals': value.lower() in ['true', 'yes', '1', 'checked']}
            else:
                print(f"[WARN] Unsupported filter for property type '{prop_type}'", file=sys.stderr)
                return None

            return filter_obj

    print(f"[WARN] Could not parse filter: {filter_str}", file=sys.stderr)
    return None


def query_notion_database(api_key, database_id, filters=None, sorts=None, page_size=100):
    """
    Query Notion database with optional filters and sorts

    Returns:
        List of pages or None on error
    """
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    body = {}
    if filters:
        body["filter"] = filters
    if sorts:
        body["sorts"] = sorts
    if page_size:
        body["page_size"] = min(page_size, 100)

    all_results = []
    has_more = True
    start_cursor = None
    page_count = 0

    while has_more:
        if start_cursor:
            body["start_cursor"] = start_cursor

        try:
            response = requests.post(url, headers=headers, json=body, timeout=30)

            if response.status_code == 200:
                data = response.json()
                all_results.extend(data.get("results", []))
                has_more = data.get("has_more", False)
                start_cursor = data.get("next_cursor")
                page_count += 1

                # Limit pagination to prevent runaway queries
                if page_count >= 10:
                    print(f"[INFO] Stopped after 10 pages ({len(all_results)} results)", file=sys.stderr)
                    break

            elif response.status_code == 401:
                print("[ERROR] 401 Unauthorized - Invalid API key", file=sys.stderr)
                return None
            elif response.status_code == 404:
                print(f"[ERROR] 404 Not Found - Database not accessible", file=sys.stderr)
                return None
            elif response.status_code == 429:
                print("[WARN] Rate limited - waiting 1 second...", file=sys.stderr)
                import time
                time.sleep(1)
                continue
            else:
                print(f"[ERROR] Query failed: {response.status_code}", file=sys.stderr)
                return None

        except requests.exceptions.Timeout:
            print("[ERROR] Request timed out", file=sys.stderr)
            return None
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Network error: {e}", file=sys.stderr)
            return None

    return all_results


def extract_property_value(prop):
    """Extract value from Notion property object"""
    if not prop:
        return None

    prop_type = prop.get("type")

    if prop_type == "title":
        text_objects = prop.get("title", [])
        return " ".join([t.get("plain_text", "") for t in text_objects])

    elif prop_type == "rich_text":
        text_objects = prop.get("rich_text", [])
        return " ".join([t.get("plain_text", "") for t in text_objects])

    elif prop_type == "number":
        return prop.get("number")

    elif prop_type == "select":
        select = prop.get("select")
        return select.get("name") if select else None

    elif prop_type == "status":
        status = prop.get("status")
        return status.get("name") if status else None

    elif prop_type == "multi_select":
        items = prop.get("multi_select", [])
        return [item.get("name") for item in items]

    elif prop_type == "date":
        date_obj = prop.get("date")
        if date_obj:
            start = date_obj.get("start", "")
            end = date_obj.get("end")
            return f"{start} → {end}" if end else start
        return None

    elif prop_type == "people":
        people = prop.get("people", [])
        return [p.get("name", p.get("id")) for p in people]

    elif prop_type == "files":
        files = prop.get("files", [])
        return [f.get("name") for f in files]

    elif prop_type == "checkbox":
        return prop.get("checkbox")

    elif prop_type == "url":
        return prop.get("url")

    elif prop_type == "email":
        return prop.get("email")

    elif prop_type == "phone_number":
        return prop.get("phone_number")

    elif prop_type == "formula":
        formula = prop.get("formula", {})
        formula_type = formula.get("type")
        return formula.get(formula_type)

    elif prop_type == "rollup":
        rollup = prop.get("rollup", {})
        rollup_type = rollup.get("type")
        if rollup_type == "array":
            return [extract_property_value(item) for item in rollup.get("array", [])]
        return rollup.get(rollup_type)

    elif prop_type == "relation":
        relations = prop.get("relation", [])
        return [r.get("id") for r in relations]

    elif prop_type in ["created_time", "last_edited_time"]:
        return prop.get(prop_type)

    elif prop_type in ["created_by", "last_edited_by"]:
        user = prop.get(prop_type, {})
        return user.get("name", user.get("id"))

    return None


def format_result(page, db_schema):
    """Format a Notion page result into readable dict"""
    props = page.get("properties", {})

    result = {
        "id": page.get("id"),
        "url": page.get("url"),
        "created": page.get("created_time"),
        "last_edited": page.get("last_edited_time"),
    }

    # Extract all properties dynamically
    for prop_name, prop_value in props.items():
        key = prop_name.lower().replace(" ", "_")
        result[key] = extract_property_value(prop_value)

    return result


def display_results(results, db_schema):
    """Display results in human-readable format"""
    # Find title property
    title_prop = None
    for prop in db_schema.get('properties', []):
        if prop['type'] == 'title':
            title_prop = prop['name']
            break

    print(f"\n[RESULTS] Found {len(results)} items\n")

    for i, result in enumerate(results, 1):
        # Get title
        title_key = title_prop.lower().replace(" ", "_") if title_prop else "title"
        title = result.get(title_key, result.get("name", "Untitled"))

        print(f"{i}. {title}")

        # Show key properties (excluding id, url, title)
        skip_keys = {'id', 'url', 'created', 'last_edited', title_key}
        for key, value in result.items():
            if key not in skip_keys and value is not None:
                if isinstance(value, list):
                    value = ", ".join(str(v) for v in value)
                print(f"   {key}: {value}")

        print(f"   URL: {result.get('url', 'N/A')}")
        print()


def main():
    """Main entry point"""
    # Configure UTF-8 output
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(
        description="Query any Notion database by name or ID",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Filter Syntax:
  --filter "Status = Active"
  --filter "Priority = High"
  --filter "Name contains project"
  --filter "Due Date < 2025-01-01"
  --filter "Tags contains Design"
  --filter "Completed is_empty"

Examples:
  # General database queries:
  python search_skill_database.py --db "Projects"
  python search_skill_database.py --db "Tasks" --filter "Status = In Progress"
  python search_skill_database.py --db "CRM" --limit 10 --json

  # Skills DB preset (supports multiple filters with AND):
  python search_skill_database.py --skills --team Solutions
  python search_skill_database.py --skills --integration "Beam AI" --name notion
        """
    )
    # General mode
    parser.add_argument("--db", help="Database name or ID to query")

    # Skills DB preset mode
    parser.add_argument("--skills", action="store_true", help="Query Beam Nexus Skills database (preset mode)")
    parser.add_argument("--team", help="[Skills mode] Filter by team (General, Solutions, Engineering, Sales)")
    parser.add_argument("--integration", help="[Skills mode] Filter by integration (Beam AI, Linear, Notion, etc.)")
    parser.add_argument("--name", help="[Skills mode] Filter by skill name (partial match)")
    parser.add_argument("--owner", help="[Skills mode] Filter by owner user ID")
    parser.add_argument("--filter", help="Filter expression (see syntax above)")
    parser.add_argument("--sort", help="Property name to sort by")
    parser.add_argument("--sort-dir", choices=["asc", "desc"], default="desc", help="Sort direction (default: desc)")
    parser.add_argument("--limit", type=int, help="Limit number of results")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    # Validate mode - either --db or --skills required
    if not args.db and not args.skills:
        print("[ERROR] Either --db or --skills is required", file=sys.stderr)
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

    # Skills DB preset mode
    if args.skills:
        # Use hardcoded Skills DB ID or from env
        skills_db_id = env_vars.get('NOTION_SKILLS_DB_ID') or '2bc2cadf-bbbc-80be-af8a-d45dfc8dfa2e'

        # Build skills-specific AND filter
        conditions = []
        if args.team:
            conditions.append({"property": "Team", "select": {"equals": args.team}})
        if args.integration:
            conditions.append({"property": "Integration", "multi_select": {"contains": args.integration}})
        if args.name:
            conditions.append({"property": "Skill Name", "title": {"contains": args.name.lower()}})
        if args.owner:
            conditions.append({"property": "Owner", "people": {"contains": args.owner}})

        # Build filter object
        if len(conditions) == 0:
            filters = None
        elif len(conditions) == 1:
            filters = conditions[0]
        else:
            filters = {"and": conditions}

        # Default sort for skills: by Created descending
        sorts = [{"property": "Created", "direction": "descending"}]
        if args.sort:
            sorts = [{"property": args.sort, "direction": "ascending" if args.sort_dir == "asc" else "descending"}]

        print(f"[INFO] Querying: Beam Nexus Skills (preset mode)", file=sys.stderr)
        if filters:
            print(f"[INFO] Filter: {json.dumps(filters)}", file=sys.stderr)

        # Query database directly
        results = query_notion_database(api_key, skills_db_id, filters, sorts)

        if results is None:
            sys.exit(1)

        # Format results with Skills DB schema
        skills_schema = {
            'name': 'Beam Nexus Skills',
            'properties': [
                {'name': 'Skill Name', 'type': 'title'},
                {'name': 'Description', 'type': 'rich_text'},
                {'name': 'Purpose', 'type': 'rich_text'},
                {'name': 'Team', 'type': 'select'},
                {'name': 'Integration', 'type': 'multi_select'},
                {'name': 'Owner', 'type': 'people'},
                {'name': 'Version', 'type': 'rich_text'},
                {'name': 'Created', 'type': 'date'},
                {'name': 'Skill', 'type': 'files'},
            ]
        }
        formatted = [format_result(page, skills_schema) for page in results]

        # Apply limit
        if args.limit and args.limit > 0:
            formatted = formatted[:args.limit]

        # Output
        if args.json:
            print(json.dumps(formatted, indent=2, default=str))
        else:
            display_results(formatted, skills_schema)

        sys.exit(0)

    # General mode - load context file
    context = load_context_file(root)

    if not context:
        print("[ERROR] No database context found", file=sys.stderr)
        print("[HINT] Run: python discover_databases.py", file=sys.stderr)
        sys.exit(2)

    # Find database
    db, matches = find_database(args.db, context)

    if not db and matches:
        print(f"[INFO] Found {len(matches)} databases matching '{args.db}':", file=sys.stderr)
        for i, m in enumerate(matches, 1):
            parent = f" ({m['parent']})" if m.get('parent') else ""
            print(f"  {i}. {m['name']}{parent}", file=sys.stderr)
        print("\nPlease be more specific or use the database ID.", file=sys.stderr)
        sys.exit(2)

    if not db:
        print(f"[ERROR] Database '{args.db}' not found in context", file=sys.stderr)
        print("[HINT] Run: python discover_databases.py --refresh", file=sys.stderr)
        sys.exit(2)

    print(f"[INFO] Querying: {db['name']}", file=sys.stderr)

    # Parse filter
    filters = None
    if args.filter:
        filters = parse_filter_expression(args.filter, db)
        if filters:
            print(f"[INFO] Filter: {json.dumps(filters)}", file=sys.stderr)

    # Build sort
    sorts = None
    if args.sort:
        sorts = [{"property": args.sort, "direction": "ascending" if args.sort_dir == "asc" else "descending"}]

    # Query database
    results = query_notion_database(api_key, db['id'], filters, sorts)

    if results is None:
        sys.exit(1)

    # Format results
    formatted = [format_result(page, db) for page in results]

    # Apply limit
    if args.limit and args.limit > 0:
        formatted = formatted[:args.limit]

    # Output
    if args.json:
        print(json.dumps(formatted, indent=2, default=str))
    else:
        display_results(formatted, db)

    sys.exit(0)


if __name__ == "__main__":
    main()
