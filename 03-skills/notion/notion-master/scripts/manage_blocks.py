#!/usr/bin/env python3
"""
Manage Notion Blocks - Get, list children, append, update, and delete blocks

Usage:
    python manage_blocks.py get --block <block_id>
    python manage_blocks.py children --block <block_id>
    python manage_blocks.py append --block <block_id> --content '<block_json>'
    python manage_blocks.py update --block <block_id> --content '<block_json>'
    python manage_blocks.py delete --block <block_id>

Examples:
    python manage_blocks.py get --block abc123-def456
    python manage_blocks.py children --page page-id-123 --limit 10
    python manage_blocks.py append --page page-id-123 --type paragraph --text "Hello world"
    python manage_blocks.py append --page page-id-123 --content '[{"type": "heading_1", "heading_1": {"rich_text": [{"text": {"content": "My Heading"}}]}}]'
    python manage_blocks.py delete --block block-id-123 --confirm

Returns:
    Exit code 0 on success, 1 on error, 2 if block not found
"""

import sys
import os
import json
import argparse
from pathlib import Path

try:
    import requests
except ImportError:
    print("[ERROR] requests library not installed", file=sys.stderr)
    print("Install with: pip install requests", file=sys.stderr)
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


def get_block(api_key, block_id):
    """
    Retrieve a block by ID

    Args:
        api_key: Notion API key
        block_id: Block ID to retrieve

    Returns:
        Block object or None on error
    """
    url = f"https://api.notion.com/v1/blocks/{block_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"[ERROR] Block not found: {block_id}", file=sys.stderr)
            return None
        elif response.status_code == 401:
            print("[ERROR] 401 Unauthorized - Invalid API key", file=sys.stderr)
            return None
        else:
            print(f"[ERROR] Failed to get block: {response.status_code}", file=sys.stderr)
            return None

    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}", file=sys.stderr)
        return None


def list_children(api_key, block_id, page_size=100, start_cursor=None):
    """
    List children blocks of a block (or page)

    Args:
        api_key: Notion API key
        block_id: Parent block/page ID
        page_size: Number of results per page (max 100)
        start_cursor: Pagination cursor

    Returns:
        Dict with 'results' and pagination info, or None on error
    """
    url = f"https://api.notion.com/v1/blocks/{block_id}/children"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28"
    }

    params = {"page_size": min(page_size, 100)}
    if start_cursor:
        params["start_cursor"] = start_cursor

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"[ERROR] Block not found: {block_id}", file=sys.stderr)
            return None
        else:
            print(f"[ERROR] Failed to list children: {response.status_code}", file=sys.stderr)
            return None

    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}", file=sys.stderr)
        return None


def append_children(api_key, block_id, children):
    """
    Append children blocks to a block (or page)

    Args:
        api_key: Notion API key
        block_id: Parent block/page ID
        children: List of block objects to append

    Returns:
        Response with created blocks, or None on error
    """
    url = f"https://api.notion.com/v1/blocks/{block_id}/children"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    body = {"children": children}

    try:
        response = requests.patch(url, headers=headers, json=body, timeout=30)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            error = response.json()
            print(f"[ERROR] Bad request: {error.get('message', 'Unknown error')}", file=sys.stderr)
            return None
        elif response.status_code == 404:
            print(f"[ERROR] Block not found: {block_id}", file=sys.stderr)
            return None
        else:
            print(f"[ERROR] Failed to append: {response.status_code}", file=sys.stderr)
            print(f"Response: {response.text}", file=sys.stderr)
            return None

    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}", file=sys.stderr)
        return None


def update_block(api_key, block_id, block_data):
    """
    Update a block's content

    Args:
        api_key: Notion API key
        block_id: Block ID to update
        block_data: Block update data

    Returns:
        Updated block or None on error
    """
    url = f"https://api.notion.com/v1/blocks/{block_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    try:
        response = requests.patch(url, headers=headers, json=block_data, timeout=30)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            error = response.json()
            print(f"[ERROR] Bad request: {error.get('message', 'Unknown error')}", file=sys.stderr)
            return None
        elif response.status_code == 404:
            print(f"[ERROR] Block not found: {block_id}", file=sys.stderr)
            return None
        else:
            print(f"[ERROR] Failed to update: {response.status_code}", file=sys.stderr)
            return None

    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}", file=sys.stderr)
        return None


def delete_block(api_key, block_id):
    """
    Delete (archive) a block

    Args:
        api_key: Notion API key
        block_id: Block ID to delete

    Returns:
        Deleted block or None on error
    """
    url = f"https://api.notion.com/v1/blocks/{block_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28"
    }

    try:
        response = requests.delete(url, headers=headers, timeout=30)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"[ERROR] Block not found: {block_id}", file=sys.stderr)
            return None
        else:
            print(f"[ERROR] Failed to delete: {response.status_code}", file=sys.stderr)
            return None

    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}", file=sys.stderr)
        return None


def build_simple_block(block_type, text, **kwargs):
    """
    Build a simple block from type and text

    Args:
        block_type: Type of block (paragraph, heading_1, heading_2, etc.)
        text: Text content
        **kwargs: Additional options (e.g., color, checked)

    Returns:
        Block object for API
    """
    # Rich text content
    rich_text = [{"type": "text", "text": {"content": text}}]

    # Handle different block types
    if block_type in ['paragraph', 'quote', 'callout']:
        return {
            "type": block_type,
            block_type: {
                "rich_text": rich_text,
                **({"color": kwargs.get('color', 'default')} if 'color' in kwargs else {})
            }
        }

    elif block_type in ['heading_1', 'heading_2', 'heading_3']:
        return {
            "type": block_type,
            block_type: {
                "rich_text": rich_text,
                "is_toggleable": kwargs.get('toggleable', False)
            }
        }

    elif block_type in ['bulleted_list_item', 'numbered_list_item']:
        return {
            "type": block_type,
            block_type: {
                "rich_text": rich_text
            }
        }

    elif block_type == 'to_do':
        return {
            "type": "to_do",
            "to_do": {
                "rich_text": rich_text,
                "checked": kwargs.get('checked', False)
            }
        }

    elif block_type == 'toggle':
        return {
            "type": "toggle",
            "toggle": {
                "rich_text": rich_text
            }
        }

    elif block_type == 'code':
        return {
            "type": "code",
            "code": {
                "rich_text": rich_text,
                "language": kwargs.get('language', 'plain text')
            }
        }

    elif block_type == 'divider':
        return {"type": "divider", "divider": {}}

    else:
        # Default to paragraph
        return {
            "type": "paragraph",
            "paragraph": {"rich_text": rich_text}
        }


def extract_block_text(block):
    """Extract plain text from a block's rich_text"""
    block_type = block.get('type', '')
    type_data = block.get(block_type, {})

    if 'rich_text' in type_data:
        texts = type_data['rich_text']
        return ''.join(t.get('plain_text', '') for t in texts)
    elif 'caption' in type_data:
        texts = type_data['caption']
        return ''.join(t.get('plain_text', '') for t in texts)

    return None


def format_block_output(block, indent=0):
    """Format a block for display"""
    prefix = "  " * indent
    block_type = block.get('type', 'unknown')
    block_id = block.get('id', '')[:8]
    has_children = block.get('has_children', False)

    text = extract_block_text(block)
    text_preview = (text[:50] + '...') if text and len(text) > 50 else text

    children_marker = " [+]" if has_children else ""

    if text_preview:
        return f"{prefix}[{block_id}] {block_type}{children_marker}: {text_preview}"
    else:
        return f"{prefix}[{block_id}] {block_type}{children_marker}"


def main():
    """Main entry point"""
    # Configure UTF-8 output
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(
        description="Manage Notion blocks (get, list, append, update, delete)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python manage_blocks.py get --block abc123
  python manage_blocks.py children --page page-id-123
  python manage_blocks.py append --page page-id-123 --type paragraph --text "Hello"
  python manage_blocks.py append --page page-id-123 --content '[{"type": "paragraph", ...}]'
  python manage_blocks.py delete --block block-id-123 --confirm
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Operation to perform')

    # Get command
    get_parser = subparsers.add_parser('get', help='Get block details')
    get_parser.add_argument("--block", required=True, help="Block ID")
    get_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    # Children command
    children_parser = subparsers.add_parser('children', help='List children blocks')
    children_parser.add_argument("--block", "--page", dest="block", required=True, help="Parent block or page ID")
    children_parser.add_argument("--limit", type=int, default=50, help="Max blocks to return")
    children_parser.add_argument("--all", action="store_true", help="Fetch all pages (handle pagination)")
    children_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    # Append command
    append_parser = subparsers.add_parser('append', help='Append blocks to a page or block')
    append_parser.add_argument("--block", "--page", dest="block", required=True, help="Parent block or page ID")
    append_parser.add_argument("--content", help="JSON array of block objects")
    append_parser.add_argument("--type", dest="block_type", help="Simple block type (paragraph, heading_1, etc.)")
    append_parser.add_argument("--text", help="Text content (used with --type)")
    append_parser.add_argument("--language", help="Code language (used with --type code)")
    append_parser.add_argument("--checked", action="store_true", help="Checked state for to_do")
    append_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    # Update command
    update_parser = subparsers.add_parser('update', help='Update a block')
    update_parser.add_argument("--block", required=True, help="Block ID to update")
    update_parser.add_argument("--content", required=True, help="JSON block update data")
    update_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a block')
    delete_parser.add_argument("--block", required=True, help="Block ID to delete")
    delete_parser.add_argument("--confirm", action="store_true", help="Skip confirmation")
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

    # Execute command
    if args.command == 'get':
        result = get_block(api_key, args.block)
        if result:
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(format_block_output(result))
                print(f"\nFull ID: {result.get('id')}")
                print(f"Type: {result.get('type')}")
                print(f"Has children: {result.get('has_children', False)}")
                print(f"Archived: {result.get('archived', False)}")
            sys.exit(0)
        else:
            sys.exit(2)

    elif args.command == 'children':
        all_results = []
        cursor = None

        while True:
            result = list_children(api_key, args.block, page_size=min(args.limit, 100), start_cursor=cursor)
            if not result:
                if not all_results:
                    sys.exit(2)
                break

            all_results.extend(result.get('results', []))

            if not args.all or not result.get('has_more'):
                break

            cursor = result.get('next_cursor')
            if len(all_results) >= args.limit:
                all_results = all_results[:args.limit]
                break

        if args.json:
            print(json.dumps(all_results, indent=2))
        else:
            print(f"Found {len(all_results)} blocks:\n")
            for block in all_results:
                print(format_block_output(block))

        sys.exit(0)

    elif args.command == 'append':
        # Build blocks to append
        if args.content:
            try:
                children = json.loads(args.content)
                if not isinstance(children, list):
                    children = [children]
            except json.JSONDecodeError as e:
                print(f"[ERROR] Invalid JSON: {e}", file=sys.stderr)
                sys.exit(1)
        elif args.block_type and args.text:
            kwargs = {}
            if args.language:
                kwargs['language'] = args.language
            if args.checked:
                kwargs['checked'] = True
            children = [build_simple_block(args.block_type, args.text, **kwargs)]
        else:
            print("[ERROR] Either --content or (--type and --text) required", file=sys.stderr)
            sys.exit(1)

        result = append_children(api_key, args.block, children)
        if result:
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                created = result.get('results', [])
                print(f"Appended {len(created)} block(s):\n")
                for block in created:
                    print(format_block_output(block))
            sys.exit(0)
        else:
            sys.exit(1)

    elif args.command == 'update':
        try:
            block_data = json.loads(args.content)
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid JSON: {e}", file=sys.stderr)
            sys.exit(1)

        result = update_block(api_key, args.block, block_data)
        if result:
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print("Block updated successfully!\n")
                print(format_block_output(result))
            sys.exit(0)
        else:
            sys.exit(1)

    elif args.command == 'delete':
        if not args.confirm:
            block = get_block(api_key, args.block)
            if block:
                print(f"About to delete block: {format_block_output(block)}")
                confirm = input("Are you sure? (yes/no): ").strip().lower()
                if confirm not in ['yes', 'y']:
                    print("Cancelled.")
                    sys.exit(0)
            else:
                sys.exit(2)

        result = delete_block(api_key, args.block)
        if result:
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print("Block deleted successfully!")
                print(f"Block ID: {args.block}")
            sys.exit(0)
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
