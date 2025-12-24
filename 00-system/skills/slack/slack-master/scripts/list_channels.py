#!/usr/bin/env python3
"""
List Slack Channels

List channels user can see using conversations.list.

Usage:
    python list_channels.py
    python list_channels.py --types "public_channel,private_channel"
    python list_channels.py --limit 50 --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def list_channels(types=None, exclude_archived=True, limit=100):
    """List channels"""
    client = get_client()

    params = {
        'exclude_archived': exclude_archived,
        'limit': min(limit, 1000)
    }

    if types:
        params['types'] = types

    # Use pagination for complete list
    if limit > 200:
        return client.paginate('conversations.list', params, limit)
    else:
        result = client.get('conversations.list', params)
        return result.get('channels', [])


def main():
    parser = argparse.ArgumentParser(description='List Slack channels')
    parser.add_argument('--types', '-t',
                        default='public_channel,private_channel',
                        help='Comma-separated: public_channel, private_channel, mpim, im')
    parser.add_argument('--include-archived', action='store_true',
                        help='Include archived channels')
    parser.add_argument('--limit', '-l', type=int, default=100,
                        help='Maximum channels to return')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        channels = list_channels(
            types=args.types,
            exclude_archived=not args.include_archived,
            limit=args.limit
        )

        if args.json:
            output = {
                'success': True,
                'count': len(channels),
                'channels': [{
                    'id': ch.get('id'),
                    'name': ch.get('name'),
                    'is_private': ch.get('is_private', False),
                    'is_member': ch.get('is_member', False),
                    'is_archived': ch.get('is_archived', False),
                    'num_members': ch.get('num_members', 0),
                    'topic': ch.get('topic', {}).get('value', ''),
                    'purpose': ch.get('purpose', {}).get('value', '')
                } for ch in channels]
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"\n{'='*60}")
            print(f"Slack Channels ({len(channels)} found)")
            print(f"{'='*60}\n")

            # Group by type
            public = [c for c in channels if not c.get('is_private')]
            private = [c for c in channels if c.get('is_private')]

            if public:
                print("Public Channels:")
                for ch in sorted(public, key=lambda x: x.get('name', '')):
                    member_status = "[member]" if ch.get('is_member') else ""
                    members = ch.get('num_members', '?')
                    print(f"  #{ch.get('name')} ({ch.get('id')}) - {members} members {member_status}")
                print()

            if private:
                print("Private Channels:")
                for ch in sorted(private, key=lambda x: x.get('name', '')):
                    members = ch.get('num_members', '?')
                    print(f"  🔒 {ch.get('name')} ({ch.get('id')}) - {members} members")
                print()

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Failed to list channels: {e}")
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
