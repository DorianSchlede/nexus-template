#!/usr/bin/env python3
"""
Open Slack Group Direct Message

Open or create a group DM with multiple users using conversations.open.

Usage:
    python open_group_dm.py @user1 @user2 @user3
    python open_group_dm.py U12345 U67890 U11111
    python open_group_dm.py --users "user1,user2,user3"
    python open_group_dm.py @user1 @user2 --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def find_user(client, identifier, user_cache=None):
    """Find user by @username, user ID, or name search"""
    if user_cache is None:
        user_cache = {}

    # If it's already a user ID
    if identifier.startswith('U') and len(identifier) == 11:
        return identifier

    # Remove @ prefix if present
    search_term = identifier.lstrip('@').lower()

    # Get all users if not cached
    if 'all_users' not in user_cache:
        result = client.get('users.list', {'limit': 1000})
        user_cache['all_users'] = result.get('members', [])

    users = user_cache['all_users']

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


def open_group_dm(user_ids):
    """Open a group DM with multiple users"""
    client = get_client()

    result = client.post('conversations.open', {'users': ','.join(user_ids)})
    return result.get('channel', {})


def main():
    parser = argparse.ArgumentParser(description='Open a group DM conversation')
    parser.add_argument('users', nargs='*',
                        help='Users to include (@username or user ID)')
    parser.add_argument('--users', '-u', dest='users_flag',
                        help='Comma-separated list of users')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    # Collect users from args
    user_inputs = args.users or []
    if args.users_flag:
        user_inputs.extend(args.users_flag.split(','))

    user_inputs = [u.strip() for u in user_inputs if u.strip()]

    if len(user_inputs) < 2:
        parser.error('Please specify at least 2 users for a group DM')

    try:
        client = get_client()
        user_cache = {}

        # Find all users
        user_ids = []
        user_names = []
        not_found = []

        for user_input in user_inputs:
            user_id = find_user(client, user_input, user_cache)
            if user_id:
                user_ids.append(user_id)
                # Get display name
                try:
                    info = client.get('users.info', {'user': user_id}).get('user', {})
                    user_names.append(info.get('real_name') or info.get('name'))
                except:
                    user_names.append(user_id)
            else:
                not_found.append(user_input)

        if not_found:
            if args.json:
                print(json.dumps({
                    'success': False,
                    'error': {'message': f'Users not found: {", ".join(not_found)}'}
                }, indent=2))
            else:
                print(f"\n[X] Users not found: {', '.join(not_found)}")
            sys.exit(1)

        # Open the group DM
        channel = open_group_dm(user_ids)
        channel_id = channel.get('id')

        if args.json:
            output = {
                'success': True,
                'channel_id': channel_id,
                'user_ids': user_ids,
                'user_names': user_names,
                'is_new': channel.get('is_new', False)
            }
            print(json.dumps(output, indent=2))
        else:
            status = '(new conversation)' if channel.get('is_new') else '(existing)'
            print(f"\n[OK] Group DM opened with {', '.join(user_names)}")
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
            print(f"\n[X] Failed to open group DM: {e}")
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
