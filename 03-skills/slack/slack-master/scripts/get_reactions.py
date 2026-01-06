#!/usr/bin/env python3
"""
Get Slack Reactions

Get reactions for a message using reactions.get.

Usage:
    python get_reactions.py --channel C123 --timestamp 1234567890.123456
    python get_reactions.py --channel C123 --timestamp 1234567890.123456 --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def get_reactions(channel, timestamp):
    """Get reactions for a message"""
    client = get_client()

    params = {
        'channel': channel,
        'timestamp': timestamp,
        'full': True
    }

    result = client.get('reactions.get', params)
    return result.get('message', {})


def main():
    parser = argparse.ArgumentParser(description='Get reactions for Slack message')
    parser.add_argument('--channel', '-c', required=True,
                        help='Channel ID')
    parser.add_argument('--timestamp', '--ts', required=True,
                        help='Message timestamp')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        message = get_reactions(
            channel=args.channel,
            timestamp=args.timestamp
        )

        reactions = message.get('reactions', [])

        if args.json:
            output = {
                'success': True,
                'channel': args.channel,
                'timestamp': args.timestamp,
                'message_text': message.get('text', '')[:100],
                'reactions': [{
                    'name': r.get('name'),
                    'count': r.get('count'),
                    'users': r.get('users', [])
                } for r in reactions]
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"\n{'='*60}")
            print(f"Reactions for message")
            print(f"{'='*60}\n")

            text_preview = message.get('text', '')[:80]
            print(f"Message: \"{text_preview}...\"" if len(message.get('text', '')) > 80 else f"Message: \"{text_preview}\"")
            print()

            if reactions:
                print("Reactions:")
                for r in reactions:
                    emoji = r.get('name')
                    count = r.get('count', 0)
                    users = r.get('users', [])
                    print(f"  :{emoji}: x{count} (by {', '.join(users[:3])}{'...' if len(users) > 3 else ''})")
            else:
                print("No reactions on this message.")

            print()

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Failed to get reactions: {e}")
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
