#!/usr/bin/env python3
"""
Pin Slack Message

Pin a message using pins.add.

Usage:
    python pin_message.py --channel C123 --timestamp 1234567890.123456
    python pin_message.py --channel C123 --timestamp 1234567890.123456 --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def pin_message(channel, timestamp):
    """Pin a message"""
    client = get_client()

    data = {
        'channel': channel,
        'timestamp': timestamp
    }

    return client.post('pins.add', data)


def main():
    parser = argparse.ArgumentParser(description='Pin a Slack message')
    parser.add_argument('--channel', '-c', required=True,
                        help='Channel ID')
    parser.add_argument('--timestamp', '--ts', required=True,
                        help='Message timestamp')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        result = pin_message(
            channel=args.channel,
            timestamp=args.timestamp
        )

        if args.json:
            output = {
                'success': True,
                'channel': args.channel,
                'timestamp': args.timestamp
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"\n[OK] Message pinned!")
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
            print(f"\n[X] Failed to pin message: {e}")
            print(f"    {explain_error(e.error_code)}")

            if e.error_code == 'already_pinned':
                print("    Hint: This message is already pinned.")
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
