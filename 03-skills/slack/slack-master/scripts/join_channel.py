#!/usr/bin/env python3
"""
Join Slack Channel

Join a public channel using conversations.join.

Usage:
    python join_channel.py --channel C123
    python join_channel.py --channel C123 --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def join_channel(channel):
    """Join a channel"""
    client = get_client()

    data = {'channel': channel}
    result = client.post('conversations.join', data)
    return result.get('channel', {})


def main():
    parser = argparse.ArgumentParser(description='Join a Slack channel')
    parser.add_argument('--channel', '-c', required=True,
                        help='Channel ID')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        channel = join_channel(args.channel)

        if args.json:
            output = {
                'success': True,
                'channel': {
                    'id': channel.get('id'),
                    'name': channel.get('name')
                }
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"\n[OK] Joined #{channel.get('name')}")
            print(f"    Channel ID: {channel.get('id')}")
            print()

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Failed to join channel: {e}")
            print(f"    {explain_error(e.error_code)}")

            if e.error_code == 'channel_not_found':
                print("    Hint: Channel may be private or doesn't exist.")
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
