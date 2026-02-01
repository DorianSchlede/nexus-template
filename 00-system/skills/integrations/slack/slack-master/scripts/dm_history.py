#!/usr/bin/env python3
"""
Get Slack DM History

Get message history from a DM conversation using conversations.history.

Usage:
    python dm_history.py @username
    python dm_history.py D12345678
    python dm_history.py @username --limit 50
    python dm_history.py @username --json
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def find_user(client, identifier):
    """Find user by @username, user ID, or name search"""
    if identifier.startswith('U') and len(identifier) == 11:
        return identifier

    search_term = identifier.lstrip('@').lower()

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


def get_dm_channel(client, user_id):
    """Get or open DM channel with user"""
    result = client.post('conversations.open', {'users': user_id})
    return result.get('channel', {}).get('id')


def get_dm_history(channel_id, limit=50):
    """Get DM message history"""
    client = get_client()

    params = {
        'channel': channel_id,
        'limit': min(limit, 1000)
    }

    result = client.get('conversations.history', params)
    return result.get('messages', [])


def format_timestamp(ts):
    """Convert Slack timestamp to readable format"""
    try:
        dt = datetime.fromtimestamp(float(ts))
        return dt.strftime('%Y-%m-%d %H:%M')
    except:
        return ts


def main():
    parser = argparse.ArgumentParser(description='Get DM message history')
    parser.add_argument('target',
                        help='DM channel ID (D...) or @username')
    parser.add_argument('--limit', '-l', type=int, default=50,
                        help='Maximum messages to return')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        client = get_client()

        # Determine if target is channel ID or user
        if args.target.startswith('D'):
            channel_id = args.target
            target_name = args.target
        else:
            # Find user and get/open DM
            user_id = find_user(client, args.target)
            if not user_id:
                if args.json:
                    print(json.dumps({
                        'success': False,
                        'error': {'message': f'User not found: {args.target}'}
                    }, indent=2))
                else:
                    print(f"\n[X] User not found: {args.target}")
                sys.exit(1)

            user_info = client.get('users.info', {'user': user_id}).get('user', {})
            target_name = user_info.get('real_name') or user_info.get('name')
            channel_id = get_dm_channel(client, user_id)

        # Get history
        messages = get_dm_history(channel_id, limit=args.limit)

        # Get user info for message authors
        user_cache = {}

        def get_user_name(uid):
            if uid not in user_cache:
                try:
                    info = client.get('users.info', {'user': uid}).get('user', {})
                    user_cache[uid] = info.get('real_name') or info.get('name') or uid
                except:
                    user_cache[uid] = uid
            return user_cache[uid]

        if args.json:
            output = {
                'success': True,
                'channel_id': channel_id,
                'target': target_name,
                'count': len(messages),
                'messages': [{
                    'ts': msg.get('ts'),
                    'user': msg.get('user'),
                    'user_name': get_user_name(msg.get('user')) if msg.get('user') else None,
                    'text': msg.get('text'),
                    'timestamp': format_timestamp(msg.get('ts'))
                } for msg in messages]
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"\n{'='*60}")
            print(f"DM History with {target_name} ({len(messages)} messages)")
            print(f"{'='*60}\n")

            # Reverse to show oldest first
            for msg in reversed(messages):
                user_name = get_user_name(msg.get('user')) if msg.get('user') else 'System'
                timestamp = format_timestamp(msg.get('ts'))
                text = msg.get('text', '')

                print(f"  [{timestamp}] {user_name}:")
                for line in text.split('\n'):
                    print(f"    {line}")
                print()

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Failed to get DM history: {e}")
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
