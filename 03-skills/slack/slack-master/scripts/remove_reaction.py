#!/usr/bin/env python3
"""
Remove Slack Reaction

Remove a reaction from a message using reactions.remove.

Usage:
    python remove_reaction.py --channel C123 --timestamp 1234567890.123456 --name thumbsup
    python remove_reaction.py --channel C123 --timestamp 1234567890.123456 --name fire --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def remove_reaction(channel, timestamp, name):
    """Remove a reaction from a message"""
    client = get_client()

    data = {
        'channel': channel,
        'timestamp': timestamp,
        'name': name.strip(':')
    }

    return client.post('reactions.remove', data)


def main():
    parser = argparse.ArgumentParser(description='Remove reaction from Slack message')
    parser.add_argument('--channel', '-c', required=True,
                        help='Channel ID')
    parser.add_argument('--timestamp', '--ts', required=True,
                        help='Message timestamp')
    parser.add_argument('--name', '-n', required=True,
                        help='Emoji name (without colons)')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        result = remove_reaction(
            channel=args.channel,
            timestamp=args.timestamp,
            name=args.name
        )

        if args.json:
            output = {
                'success': True,
                'channel': args.channel,
                'timestamp': args.timestamp,
                'reaction': args.name.strip(':')
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"\n[OK] Removed :{args.name.strip(':')}:")
            print(f"    Channel: {args.channel}")
            print(f"    Message: {args.timestamp}")
            print()

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Failed to remove reaction: {e}")
            print(f"    {explain_error(e.error_code)}")

            if e.error_code == 'no_reaction':
                print("    Hint: You haven't added this reaction.")
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
