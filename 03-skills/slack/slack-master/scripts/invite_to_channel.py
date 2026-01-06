#!/usr/bin/env python3
"""
Invite Users to Slack Channel

Invite users to a channel using conversations.invite.

Usage:
    python invite_to_channel.py --channel C123 --users U123,U456
    python invite_to_channel.py --channel C123 --users U123 --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def invite_to_channel(channel, users):
    """Invite users to a channel"""
    client = get_client()

    data = {
        'channel': channel,
        'users': users
    }

    result = client.post('conversations.invite', data)
    return result.get('channel', {})


def main():
    parser = argparse.ArgumentParser(description='Invite users to Slack channel')
    parser.add_argument('--channel', '-c', required=True,
                        help='Channel ID')
    parser.add_argument('--users', '-u', required=True,
                        help='Comma-separated user IDs')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        channel = invite_to_channel(
            channel=args.channel,
            users=args.users
        )

        if args.json:
            output = {
                'success': True,
                'channel': {
                    'id': channel.get('id'),
                    'name': channel.get('name')
                },
                'invited_users': args.users.split(',')
            }
            print(json.dumps(output, indent=2))
        else:
            user_count = len(args.users.split(','))
            print(f"\n[OK] Invited {user_count} user(s) to #{channel.get('name')}")
            print(f"    Channel ID: {channel.get('id')}")
            print()

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Failed to invite users: {e}")
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
