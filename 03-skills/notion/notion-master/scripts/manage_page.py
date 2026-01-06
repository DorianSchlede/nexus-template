#!/usr/bin/env python3
"""
Manage Notion Pages - Get, Update, and Delete page operations

Usage:
    python manage_page.py get --page <page_id>
    python manage_page.py update --page <page_id> --properties '{"Status": "Done"}'
    python manage_page.py delete --page <page_id>

Examples:
    python manage_page.py get --page abc123-def456
    python manage_page.py update --page abc123 --properties '{"Priority": "High", "Status": "In Progress"}'
    python manage_page.py delete --page abc123 --confirm

Returns:
    Exit code 0 on success, 1 on error, 2 if page not found
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


def get_page(api_key, page_id):
    """
    Retrieve a page by ID

    Args:
        api_key: Notion API key
        page_id: Page ID to retrieve

    Returns:
        Page object or None on error
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
            print("[ERROR] 401 Unauthorized - Invalid API key", file=sys.stderr)
            return None
        else:
            print(f"[ERROR] Failed to get page: {response.status_code}", file=sys.stderr)
            print(f"Response: {response.text}", file=sys.stderr)
            return None

    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}", file=sys.stderr)
        return None


def build_property_value(prop_type, value):
    """
    Build Notion property value from user input

    Args:
        prop_type: Property type string
        value: User-provided value

    Returns:
        Notion API property value or None if invalid
    """
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
        return {"select": {"name": str(value)}}

    elif prop_type == 'multi_select':
        if isinstance(value, str):
            values = [v.strip() for v in value.split(',')]
        else:
            values = value
        return {"multi_select": [{"name": v} for v in values]}

    elif prop_type == 'status':
        return {"status": {"name": str(value)}}

    elif prop_type == 'date':
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
        if isinstance(value, str):
            user_ids = [v.strip() for v in value.split(',')]
        else:
            user_ids = value
        return {"people": [{"id": uid} for uid in user_ids]}

    elif prop_type == 'relation':
        if isinstance(value, str):
            page_ids = [v.strip() for v in value.split(',')]
        else:
            page_ids = value
        return {"relation": [{"id": pid} for pid in page_ids]}

    else:
        # For unknown types, try as rich_text
        return {"rich_text": [{"text": {"content": str(value)}}]}


def update_page(api_key, page_id, properties, context=None):
    """
    Update a page's properties

    Args:
        api_key: Notion API key
        page_id: Page ID to update
        properties: Dict of property name → value
        context: Optional context with database schemas

    Returns:
        Updated page object or None on error
    """
    # First get the page to understand its properties
    page = get_page(api_key, page_id)
    if not page:
        return None

    # Build API properties
    api_props = {}
    page_props = page.get('properties', {})

    for name, value in properties.items():
        # Find the property in the page
        matching_prop = None
        for prop_name, prop_data in page_props.items():
            if prop_name.lower() == name.lower():
                matching_prop = (prop_name, prop_data)
                break

        if not matching_prop:
            print(f"[WARN] Property '{name}' not found in page, skipping", file=sys.stderr)
            continue

        prop_name, prop_data = matching_prop
        prop_type = prop_data.get('type')

        prop_value = build_property_value(prop_type, value)
        if prop_value:
            api_props[prop_name] = prop_value

    if not api_props:
        print("[ERROR] No valid properties to update", file=sys.stderr)
        return None

    # Update the page
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    body = {"properties": api_props}

    try:
        response = requests.patch(url, headers=headers, json=body, timeout=30)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            error = response.json()
            print(f"[ERROR] Bad request: {error.get('message', 'Unknown error')}", file=sys.stderr)
            return None
        elif response.status_code == 404:
            print(f"[ERROR] Page not found: {page_id}", file=sys.stderr)
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


def delete_page(api_key, page_id):
    """
    Archive (delete) a page

    Args:
        api_key: Notion API key
        page_id: Page ID to archive

    Returns:
        Archived page object or None on error
    """
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    body = {"archived": True}

    try:
        response = requests.patch(url, headers=headers, json=body, timeout=30)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"[ERROR] Page not found: {page_id}", file=sys.stderr)
            return None
        elif response.status_code == 401:
            print("[ERROR] 401 Unauthorized - Invalid API key", file=sys.stderr)
            return None
        else:
            print(f"[ERROR] Delete failed: {response.status_code}", file=sys.stderr)
            print(f"Response: {response.text}", file=sys.stderr)
            return None

    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}", file=sys.stderr)
        return None


def extract_property_value(prop_data):
    """Extract displayable value from property data"""
    prop_type = prop_data.get('type')

    if prop_type == 'title':
        texts = prop_data.get('title', [])
        return ''.join(t.get('plain_text', '') for t in texts) or '[Untitled]'

    elif prop_type == 'rich_text':
        texts = prop_data.get('rich_text', [])
        return ''.join(t.get('plain_text', '') for t in texts) or ''

    elif prop_type == 'number':
        return prop_data.get('number')

    elif prop_type == 'select':
        sel = prop_data.get('select')
        return sel.get('name') if sel else None

    elif prop_type == 'multi_select':
        options = prop_data.get('multi_select', [])
        return ', '.join(o.get('name', '') for o in options) or None

    elif prop_type == 'status':
        status = prop_data.get('status')
        return status.get('name') if status else None

    elif prop_type == 'date':
        date_obj = prop_data.get('date')
        if date_obj:
            start = date_obj.get('start', '')
            end = date_obj.get('end')
            return f"{start} → {end}" if end else start
        return None

    elif prop_type == 'checkbox':
        return 'Yes' if prop_data.get('checkbox') else 'No'

    elif prop_type == 'url':
        return prop_data.get('url')

    elif prop_type == 'email':
        return prop_data.get('email')

    elif prop_type == 'phone_number':
        return prop_data.get('phone_number')

    elif prop_type == 'people':
        people = prop_data.get('people', [])
        return ', '.join(p.get('name', p.get('id', '')) for p in people) or None

    elif prop_type == 'relation':
        relations = prop_data.get('relation', [])
        return f"{len(relations)} linked" if relations else None

    elif prop_type == 'formula':
        formula = prop_data.get('formula', {})
        formula_type = formula.get('type')
        return formula.get(formula_type)

    elif prop_type == 'rollup':
        rollup = prop_data.get('rollup', {})
        rollup_type = rollup.get('type')
        if rollup_type == 'array':
            return f"{len(rollup.get('array', []))} items"
        return rollup.get(rollup_type)

    elif prop_type == 'created_time':
        return prop_data.get('created_time', '')[:10]

    elif prop_type == 'last_edited_time':
        return prop_data.get('last_edited_time', '')[:10]

    elif prop_type == 'created_by':
        user = prop_data.get('created_by', {})
        return user.get('name', user.get('id', ''))

    elif prop_type == 'last_edited_by':
        user = prop_data.get('last_edited_by', {})
        return user.get('name', user.get('id', ''))

    elif prop_type == 'files':
        files = prop_data.get('files', [])
        return f"{len(files)} files" if files else None

    else:
        return f"[{prop_type}]"


def format_page_output(page):
    """Format page data for display"""
    output = []

    # Page metadata
    page_id = page.get('id', 'Unknown')
    url = page.get('url', '')
    created = page.get('created_time', '')[:10]
    edited = page.get('last_edited_time', '')[:10]
    archived = page.get('archived', False)

    output.append(f"Page ID: {page_id}")
    output.append(f"URL: {url}")
    output.append(f"Created: {created}")
    output.append(f"Last Edited: {edited}")
    if archived:
        output.append("Status: ARCHIVED")
    output.append("")

    # Properties
    output.append("Properties:")
    output.append("-" * 40)

    props = page.get('properties', {})
    for name, data in sorted(props.items()):
        prop_type = data.get('type', 'unknown')
        value = extract_property_value(data)
        if value is not None:
            output.append(f"  {name} ({prop_type}): {value}")
        else:
            output.append(f"  {name} ({prop_type}): [empty]")

    return '\n'.join(output)


def main():
    """Main entry point"""
    # Configure UTF-8 output
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(
        description="Manage Notion pages (get, update, delete)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python manage_page.py get --page abc123-def456
  python manage_page.py update --page abc123 --properties '{"Status": "Done"}'
  python manage_page.py delete --page abc123 --confirm
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Operation to perform')

    # Get command
    get_parser = subparsers.add_parser('get', help='Get page details')
    get_parser.add_argument("--page", required=True, help="Page ID")
    get_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    # Update command
    update_parser = subparsers.add_parser('update', help='Update page properties')
    update_parser.add_argument("--page", required=True, help="Page ID")
    update_parser.add_argument("--properties", required=True, help="JSON object with property values")
    update_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Archive (delete) a page')
    delete_parser.add_argument("--page", required=True, help="Page ID")
    delete_parser.add_argument("--confirm", action="store_true", help="Skip confirmation prompt")
    delete_parser.add_argument("--json", action="store_true", help="Output raw JSON")

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

    # Load context for schema info
    context = load_context_file(root)

    # Execute command
    if args.command == 'get':
        result = get_page(api_key, args.page)
        if result:
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(format_page_output(result))
            sys.exit(0)
        else:
            sys.exit(2)

    elif args.command == 'update':
        try:
            properties = json.loads(args.properties)
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid JSON: {e}", file=sys.stderr)
            sys.exit(1)

        result = update_page(api_key, args.page, properties, context)
        if result:
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print("\n" + "=" * 50)
                print("Page updated successfully!")
                print("=" * 50 + "\n")
                print(format_page_output(result))
            sys.exit(0)
        else:
            sys.exit(1)

    elif args.command == 'delete':
        if not args.confirm:
            # Get page info first
            page = get_page(api_key, args.page)
            if page:
                props = page.get('properties', {})
                title = '[Untitled]'
                for name, data in props.items():
                    if data.get('type') == 'title':
                        title = extract_property_value(data)
                        break
                print(f"About to archive page: {title}")
                print(f"Page ID: {args.page}")
                confirm = input("Are you sure? (yes/no): ").strip().lower()
                if confirm not in ['yes', 'y']:
                    print("Cancelled.")
                    sys.exit(0)
            else:
                sys.exit(2)

        result = delete_page(api_key, args.page)
        if result:
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print("\n" + "=" * 50)
                print("Page archived successfully!")
                print("=" * 50)
                print(f"Page ID: {args.page}")
                print("Note: Archived pages can be restored in Notion.")
            sys.exit(0)
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
