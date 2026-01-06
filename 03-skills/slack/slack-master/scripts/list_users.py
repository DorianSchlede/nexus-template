#!/usr/bin/env python3
"""
List Slack Users

List workspace users using users.list.

Usage:
    python list_users.py
    python list_users.py --limit 50
    python list_users.py --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def list_users(limit=100):
    """List workspace users"""
    client = get_client()

    params = {'limit': min(limit, 1000)}

    if limit > 200:
        return client.paginate('users.list', params, limit)
    else:
        result = client.get('users.list', params)
        return result.get('members', [])


def main():
    parser = argparse.ArgumentParser(description='List Slack users')
    parser.add_argument('--limit', '-l', type=int, default=100,
                        help='Maximum users to return')
    parser.add_argument('--include-bots', action='store_true',
                        help='Include bot users')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        users = list_users(limit=args.limit)

        # Filter out bots unless requested
        if not args.include_bots:
            users = [u for u in users if not u.get('is_bot') and u.get('id') != 'USLACKBOT']

        if args.json:
            output = {
                'success': True,
                'count': len(users),
                'users': [{
                    'id': u.get('id'),
                    'name': u.get('name'),
                    'real_name': u.get('real_name'),
                    'display_name': u.get('profile', {}).get('display_name'),
                    'email': u.get('profile', {}).get('email'),
                    'is_admin': u.get('is_admin', False),
                    'is_owner': u.get('is_owner', False),
                    'is_bot': u.get('is_bot', False),
                    'deleted': u.get('deleted', False),
                    'status_text': u.get('profile', {}).get('status_text'),
                    'status_emoji': u.get('profile', {}).get('status_emoji')
                } for u in users]
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"\n{'='*60}")
            print(f"Workspace Users ({len(users)} found)")
            print(f"{'='*60}\n")

            # Sort by real name
            users_sorted = sorted(users, key=lambda x: x.get('real_name', x.get('name', '')))

            for user in users_sorted:
                name = user.get('real_name') or user.get('name')
                username = user.get('name')
                user_id = user.get('id')

                status = []
                if user.get('is_admin'):
                    status.append('admin')
                if user.get('is_owner'):
                    status.append('owner')
                if user.get('deleted'):
                    status.append('deactivated')

                status_str = f" [{', '.join(status)}]" if status else ""

                # Show status emoji if set
                status_emoji = user.get('profile', {}).get('status_emoji', '')

                print(f"  {status_emoji} {name} (@{username}) - {user_id}{status_str}")

            print()

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Failed to list users: {e}")
            print(f"    {explain_error(e.error_code)}")
        sys.exit(1)
    except Exception as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': {'message': str(e)}
            }, indent=2))
        else:
            print(f"\n[X] Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
