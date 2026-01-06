#!/usr/bin/env python3
"""
Add Slack Reaction

Add a reaction to a message using reactions.add.

Usage:
    python add_reaction.py --channel C123 --timestamp 1234567890.123456 --name thumbsup
    python add_reaction.py --channel C123 --timestamp 1234567890.123456 --name fire --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def add_reaction(channel, timestamp, name):
    """Add a reaction to a message"""
    client = get_client()

    data = {
        'channel': channel,
        'timestamp': timestamp,
        'name': name.strip(':')  # Remove colons if provided
    }

    return client.post('reactions.add', data)


def main():
    parser = argparse.ArgumentParser(description='Add reaction to Slack message')
    parser.add_argument('--channel', '-c', required=True,
                        help='Channel ID')
    parser.add_argument('--timestamp', '--ts', required=True,
                        help='Message timestamp')
    parser.add_argument('--name', '-n', required=True,
                        help='Emoji name (without colons, e.g., thumbsup)')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        result = add_reaction(
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
            print(f"\n[OK] Added :{args.name.strip(':')}:")
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
            print(f"\n[X] Failed to add reaction: {e}")
            print(f"    {explain_error(e.error_code)}")

            if e.error_code == 'already_reacted':
                print("    Hint: You've already added this reaction.")
            elif e.error_code == 'invalid_name':
                print("    Hint: Emoji name not found. Check spelling.")
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
