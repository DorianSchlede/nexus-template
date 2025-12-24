#!/usr/bin/env python3
"""
Open Slack Direct Message

Open or get a DM conversation with a user using conversations.open.

Usage:
    python open_dm.py @username
    python open_dm.py U12345678
    python open_dm.py --user "John Doe"
    python open_dm.py @username --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def find_user(client, identifier):
    """Find user by @username, user ID, or name search"""
    # If it's already a user ID
    if identifier.startswith('U') and len(identifier) == 11:
        return identifier

    # Remove @ prefix if present
    search_term = identifier.lstrip('@').lower()

    # Get all users and search
    result = client.get('users.list', {'limit': 1000})
    users = result.get('members', [])

    for user in users:
        if user.get('deleted'):
            continue

        username = user.get('name', '').lower()
        display_name = user.get('profile', {}).get('display_name', '').lower()
        real_name = user.get('real_name', '').lower()

        if (search_term == username or
            search_term == display_name or
            search_term in real_name or
            search_term in username):
            return user.get('id')

    return None


def open_dm(user_id):
    """Open a DM conversation with a user"""
    client = get_client()

    result = client.post('conversations.open', {'users': user_id})
    return result.get('channel', {})


def main():
    parser = argparse.ArgumentParser(description='Open a DM conversation')
    parser.add_argument('user', nargs='?',
                        help='User to DM (@username, user ID, or name)')
    parser.add_argument('--user', '-u', dest='user_flag',
                        help='User to DM (alternative)')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    user_input = args.user or args.user_flag
    if not user_input:
        parser.error('Please specify a user (@username, user ID, or name)')

    try:
        client = get_client()

        # Find the user
        user_id = find_user(client, user_input)
        if not user_id:
            if args.json:
                print(json.dumps({
                    'success': False,
                    'error': {'message': f'User not found: {user_input}'}
                }, indent=2))
            else:
                print(f"\n[X] User not found: {user_input}")
            sys.exit(1)

        # Get user info for display
        user_info = client.get('users.info', {'user': user_id}).get('user', {})
        user_name = user_info.get('real_name') or user_info.get('name')

        # Open the DM
        channel = open_dm(user_id)
        channel_id = channel.get('id')

        if args.json:
            output = {
                'success': True,
                'channel_id': channel_id,
                'user_id': user_id,
                'user_name': user_name,
                'is_new': channel.get('is_new', False)
            }
            print(json.dumps(output, indent=2))
        else:
            status = '(new conversation)' if channel.get('is_new') else '(existing)'
            print(f"\n[OK] DM opened with {user_name} (@{user_info.get('name')})")
            print(f"     Channel ID: {channel_id} {status}")
            print(f"\n     Use this channel ID to send messages:")
            print(f"     python send_message.py {channel_id} \"Your message\"\n")

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Failed to open DM: {e}")
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
