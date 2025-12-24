#!/usr/bin/env python3
"""
Get Slack Channel Info

Get detailed information about a channel using conversations.info.

Usage:
    python channel_info.py --channel C123
    python channel_info.py --channel C123 --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def get_channel_info(channel, include_num_members=True):
    """Get channel information"""
    client = get_client()

    params = {
        'channel': channel,
        'include_num_members': include_num_members
    }

    result = client.get('conversations.info', params)
    return result.get('channel', {})


def main():
    parser = argparse.ArgumentParser(description='Get Slack channel info')
    parser.add_argument('--channel', '-c', required=True,
                        help='Channel ID')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        channel = get_channel_info(args.channel)

        if args.json:
            output = {
                'success': True,
                'channel': {
                    'id': channel.get('id'),
                    'name': channel.get('name'),
                    'is_channel': channel.get('is_channel', False),
                    'is_private': channel.get('is_private', False),
                    'is_member': channel.get('is_member', False),
                    'is_archived': channel.get('is_archived', False),
                    'num_members': channel.get('num_members', 0),
                    'topic': channel.get('topic', {}).get('value', ''),
                    'purpose': channel.get('purpose', {}).get('value', ''),
                    'creator': channel.get('creator'),
                    'created': channel.get('created')
                }
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"\n{'='*60}")
            prefix = "🔒 " if channel.get('is_private') else "#"
            print(f"Channel: {prefix}{channel.get('name')}")
            print(f"{'='*60}\n")

            print(f"ID: {channel.get('id')}")
            print(f"Type: {'Private' if channel.get('is_private') else 'Public'} Channel")
            print(f"Members: {channel.get('num_members', 'Unknown')}")
            print(f"Your Status: {'Member' if channel.get('is_member') else 'Not a member'}")
            print(f"Archived: {'Yes' if channel.get('is_archived') else 'No'}")

            if channel.get('topic', {}).get('value'):
                print(f"\nTopic: {channel['topic']['value']}")

            if channel.get('purpose', {}).get('value'):
                print(f"Purpose: {channel['purpose']['value']}")

            if channel.get('created'):
                from datetime import datetime
                created = datetime.fromtimestamp(channel['created'])
                print(f"\nCreated: {created.strftime('%Y-%m-%d')}")

            print()

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Failed to get channel info: {e}")
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
