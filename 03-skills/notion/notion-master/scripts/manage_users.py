#!/usr/bin/env python3
"""
Manage Notion Users - List, get, and retrieve current user

Usage:
    python manage_users.py list
    python manage_users.py get --user <user_id>
    python manage_users.py me

Examples:
    python manage_users.py list --limit 50
    python manage_users.py get --user abc123-def456
    python manage_users.py me --json

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

try:
    import yaml
except ImportError:
    yaml = None


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


def list_users(api_key, page_size=100, start_cursor=None):
    """
    List all users in the workspace

    Args:
        api_key: Notion API key
        page_size: Number of results per page (max 100)
        start_cursor: Pagination cursor

    Returns:
        Dict with 'results' and pagination info, or None on error
    """
    url = "https://api.notion.com/v1/users"
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
        elif response.status_code == 401:
            print("[ERROR] 401 Unauthorized - Invalid API key", file=sys.stderr)
            return None
        else:
            print(f"[ERROR] Failed to list users: {response.status_code}", file=sys.stderr)
            return None

    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}", file=sys.stderr)
        return None


def get_user(api_key, user_id):
    """
    Get a specific user by ID

    Args:
        api_key: Notion API key
        user_id: User ID to retrieve

    Returns:
        User object or None on error
    """
    url = f"https://api.notion.com/v1/users/{user_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"[ERROR] User not found: {user_id}", file=sys.stderr)
            return None
        elif response.status_code == 401:
            print("[ERROR] 401 Unauthorized - Invalid API key", file=sys.stderr)
            return None
        else:
            print(f"[ERROR] Failed to get user: {response.status_code}", file=sys.stderr)
            return None

    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}", file=sys.stderr)
        return None


def get_me(api_key):
    """
    Get the current bot user (the integration)

    Args:
        api_key: Notion API key

    Returns:
        Bot user object or None on error
    """
    url = "https://api.notion.com/v1/users/me"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            print("[ERROR] 401 Unauthorized - Invalid API key", file=sys.stderr)
            return None
        else:
            print(f"[ERROR] Failed to get current user: {response.status_code}", file=sys.stderr)
            return None

    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}", file=sys.stderr)
        return None


def format_user(user):
    """Format a user object for display"""
    user_type = user.get('type', 'unknown')
    user_id = user.get('id', '')
    name = user.get('name', 'Unknown')
    email = ''

    if user_type == 'person':
        email = user.get('person', {}).get('email', '')
    elif user_type == 'bot':
        owner = user.get('bot', {}).get('owner', {})
        owner_type = owner.get('type', '')
        if owner_type == 'workspace':
            email = '[workspace bot]'
        elif owner_type == 'user':
            email = f"[owned by user]"

    avatar = user.get('avatar_url', '')
    avatar_indicator = " 📷" if avatar else ""

    return {
        'id': user_id,
        'name': name,
        'type': user_type,
        'email': email,
        'has_avatar': bool(avatar)
    }


def save_users_to_context(users, root_path):
    """Save users to context file for @mention support"""
    if yaml is None:
        print("[WARN] PyYAML not installed, skipping context file update", file=sys.stderr)
        return

    context_file = root_path / "01-memory" / "integrations" / "notion-users.yaml"
    context_file.parent.mkdir(parents=True, exist_ok=True)

    from datetime import datetime

    data = {
        'last_synced': datetime.now().isoformat(),
        'user_count': len(users),
        'users': [format_user(u) for u in users]
    }

    try:
        with open(context_file, 'w', encoding='utf-8') as f:
            f.write("---\n")
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            f.write("---\n\n")
            f.write("# Notion Users Context\n\n")
            f.write("Auto-generated by notion-connect skill.\n")
            f.write("Use user IDs for @mentions and people properties.\n")

        print(f"\n[INFO] Saved {len(users)} users to: {context_file}", file=sys.stderr)

    except Exception as e:
        print(f"[WARN] Failed to save context file: {e}", file=sys.stderr)


def main():
    """Main entry point"""
    # Configure UTF-8 output
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(
        description="Manage Notion users (list, get, me)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python manage_users.py list
  python manage_users.py get --user abc123-def456
  python manage_users.py me
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Operation to perform')

    # List command
    list_parser = subparsers.add_parser('list', help='List all users')
    list_parser.add_argument("--limit", type=int, default=100, help="Max users to return")
    list_parser.add_argument("--all", action="store_true", help="Fetch all pages")
    list_parser.add_argument("--save", action="store_true", help="Save to context file")
    list_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    # Get command
    get_parser = subparsers.add_parser('get', help='Get a specific user')
    get_parser.add_argument("--user", required=True, help="User ID")
    get_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    # Me command
    me_parser = subparsers.add_parser('me', help='Get current bot user')
    me_parser.add_argument("--json", action="store_true", help="Output raw JSON")

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
        all_users = []
        cursor = None

        while True:
            result = list_users(api_key, page_size=min(args.limit, 100), start_cursor=cursor)
            if not result:
                if not all_users:
                    sys.exit(1)
                break

            all_users.extend(result.get('results', []))

            if not args.all or not result.get('has_more'):
                break

            cursor = result.get('next_cursor')
            if len(all_users) >= args.limit:
                all_users = all_users[:args.limit]
                break

        if args.json:
            print(json.dumps(all_users, indent=2))
        else:
            print(f"Found {len(all_users)} users:\n")
            print(f"{'ID':<40} {'Type':<8} {'Name':<25} {'Email/Info'}")
            print("-" * 100)
            for user in all_users:
                info = format_user(user)
                print(f"{info['id']:<40} {info['type']:<8} {info['name']:<25} {info['email']}")

        if args.save:
            save_users_to_context(all_users, root)

        sys.exit(0)

    elif args.command == 'get':
        result = get_user(api_key, args.user)
        if result:
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                info = format_user(result)
                print(f"User ID: {info['id']}")
                print(f"Name: {info['name']}")
                print(f"Type: {info['type']}")
                if info['email']:
                    print(f"Email/Info: {info['email']}")
                if result.get('avatar_url'):
                    print(f"Avatar: {result['avatar_url']}")
            sys.exit(0)
        else:
            sys.exit(1)

    elif args.command == 'me':
        result = get_me(api_key)
        if result:
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                info = format_user(result)
                print("Current Bot User:")
                print(f"  ID: {info['id']}")
                print(f"  Name: {info['name']}")
                print(f"  Type: {info['type']}")

                bot_info = result.get('bot', {})
                owner = bot_info.get('owner', {})
                if owner.get('type') == 'workspace':
                    print(f"  Owner: Workspace ({owner.get('workspace', True)})")
                elif owner.get('type') == 'user':
                    print(f"  Owner: User")
            sys.exit(0)
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
