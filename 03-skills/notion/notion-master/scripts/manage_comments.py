#!/usr/bin/env python3
"""
Manage Notion Comments - Create, list, and retrieve comments

Usage:
    python manage_comments.py list --block <block_id>
    python manage_comments.py list --page <page_id>
    python manage_comments.py create --page <page_id> --text "Comment text"
    python manage_comments.py create --discussion <discussion_id> --text "Reply text"
    python manage_comments.py get --comment <comment_id>

Examples:
    python manage_comments.py list --page abc123-def456
    python manage_comments.py create --page abc123 --text "Great work on this!"
    python manage_comments.py create --discussion thread-id --text "I agree!"

Returns:
    Exit code 0 on success, 1 on error
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


def list_comments(api_key, block_id=None, page_size=100, start_cursor=None):
    """
    List comments on a block or page

    Args:
        api_key: Notion API key
        block_id: Block ID to get comments for
        page_size: Number of results per page (max 100)
        start_cursor: Pagination cursor

    Returns:
        Dict with 'results' and pagination info, or None on error
    """
    url = "https://api.notion.com/v1/comments"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28"
    }

    params = {"page_size": min(page_size, 100)}
    if block_id:
        params["block_id"] = block_id
    if start_cursor:
        params["start_cursor"] = start_cursor

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            error = response.json()
            print(f"[ERROR] Bad request: {error.get('message', 'Unknown')}", file=sys.stderr)
            return None
        elif response.status_code == 401:
            print("[ERROR] 401 Unauthorized - Invalid API key", file=sys.stderr)
            return None
        elif response.status_code == 404:
            print(f"[ERROR] Block/page not found", file=sys.stderr)
            return None
        else:
            print(f"[ERROR] Failed to list comments: {response.status_code}", file=sys.stderr)
            print(f"Response: {response.text}", file=sys.stderr)
            return None

    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}", file=sys.stderr)
        return None


def create_comment(api_key, text, page_id=None, discussion_id=None):
    """
    Create a new comment

    Args:
        api_key: Notion API key
        text: Comment text content
        page_id: Page ID to comment on (for new discussion)
        discussion_id: Discussion ID to reply to

    Returns:
        Created comment object or None on error
    """
    url = "https://api.notion.com/v1/comments"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    # Build rich text
    rich_text = [{"type": "text", "text": {"content": text}}]

    body = {"rich_text": rich_text}

    if page_id:
        body["parent"] = {"page_id": page_id}
    elif discussion_id:
        body["discussion_id"] = discussion_id
    else:
        print("[ERROR] Either --page or --discussion is required", file=sys.stderr)
        return None

    try:
        response = requests.post(url, headers=headers, json=body, timeout=30)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            error = response.json()
            print(f"[ERROR] Bad request: {error.get('message', 'Unknown')}", file=sys.stderr)
            return None
        elif response.status_code == 401:
            print("[ERROR] 401 Unauthorized - Invalid API key", file=sys.stderr)
            return None
        elif response.status_code == 404:
            print(f"[ERROR] Page/discussion not found", file=sys.stderr)
            return None
        else:
            print(f"[ERROR] Failed to create comment: {response.status_code}", file=sys.stderr)
            print(f"Response: {response.text}", file=sys.stderr)
            return None

    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}", file=sys.stderr)
        return None


def get_comment(api_key, comment_id):
    """
    Get a specific comment by ID

    Note: The Notion API doesn't have a direct get comment endpoint.
    This would require listing and filtering.

    Args:
        api_key: Notion API key
        comment_id: Comment ID to retrieve

    Returns:
        Comment object or None
    """
    # Notion API doesn't have GET /comments/{id}
    # We would need to know the parent block/page to list and filter
    print("[WARN] Direct comment retrieval not supported by Notion API", file=sys.stderr)
    print("[HINT] Use 'list --block <block_id>' to find comments", file=sys.stderr)
    return None


def extract_comment_text(comment):
    """Extract plain text from comment's rich_text"""
    rich_text = comment.get('rich_text', [])
    return ''.join(t.get('plain_text', '') for t in rich_text)


def format_comment(comment):
    """Format a comment for display"""
    comment_id = comment.get('id', '')[:8]
    created = comment.get('created_time', '')[:10]
    text = extract_comment_text(comment)
    text_preview = (text[:60] + '...') if len(text) > 60 else text

    # Get author info
    author = comment.get('created_by', {})
    author_name = author.get('name', 'Unknown')

    discussion_id = comment.get('discussion_id', '')[:8]

    return {
        'id': comment.get('id'),
        'short_id': comment_id,
        'author': author_name,
        'created': created,
        'text': text,
        'text_preview': text_preview,
        'discussion_id': discussion_id
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
        description="Manage Notion comments (list, create)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python manage_comments.py list --page abc123
  python manage_comments.py create --page abc123 --text "Great work!"
  python manage_comments.py create --discussion thread-id --text "I agree!"
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Operation to perform')

    # List command
    list_parser = subparsers.add_parser('list', help='List comments')
    list_parser.add_argument("--block", "--page", dest="block", required=True, help="Block or page ID")
    list_parser.add_argument("--limit", type=int, default=50, help="Max comments to return")
    list_parser.add_argument("--all", action="store_true", help="Fetch all pages")
    list_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    # Create command
    create_parser = subparsers.add_parser('create', help='Create a comment')
    create_parser.add_argument("--page", help="Page ID for new discussion")
    create_parser.add_argument("--discussion", help="Discussion ID to reply to")
    create_parser.add_argument("--text", required=True, help="Comment text")
    create_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    # Get command (limited support)
    get_parser = subparsers.add_parser('get', help='Get a comment (limited)')
    get_parser.add_argument("--comment", required=True, help="Comment ID")
    get_parser.add_argument("--json", action="store_true", help="Output raw JSON")

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
    if args.command == 'list':
        all_comments = []
        cursor = None

        while True:
            result = list_comments(api_key, block_id=args.block, page_size=min(args.limit, 100), start_cursor=cursor)
            if not result:
                if not all_comments:
                    sys.exit(1)
                break

            all_comments.extend(result.get('results', []))

            if not args.all or not result.get('has_more'):
                break

            cursor = result.get('next_cursor')
            if len(all_comments) >= args.limit:
                all_comments = all_comments[:args.limit]
                break

        if args.json:
            print(json.dumps(all_comments, indent=2))
        else:
            if not all_comments:
                print("No comments found.")
            else:
                print(f"Found {len(all_comments)} comments:\n")
                for comment in all_comments:
                    info = format_comment(comment)
                    print(f"[{info['short_id']}] {info['author']} ({info['created']}):")
                    print(f"    {info['text_preview']}")
                    print(f"    Discussion: {info['discussion_id']}")
                    print()

        sys.exit(0)

    elif args.command == 'create':
        if not args.page and not args.discussion:
            print("[ERROR] Either --page or --discussion is required", file=sys.stderr)
            sys.exit(1)

        result = create_comment(api_key, args.text, page_id=args.page, discussion_id=args.discussion)
        if result:
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                info = format_comment(result)
                print("Comment created successfully!")
                print(f"  ID: {info['id']}")
                print(f"  Author: {info['author']}")
                print(f"  Discussion: {info['discussion_id']}")
                print(f"  Text: {info['text_preview']}")
            sys.exit(0)
        else:
            sys.exit(1)

    elif args.command == 'get':
        result = get_comment(api_key, args.comment)
        if result:
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                info = format_comment(result)
                print(f"Comment: {info['text']}")
            sys.exit(0)
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
