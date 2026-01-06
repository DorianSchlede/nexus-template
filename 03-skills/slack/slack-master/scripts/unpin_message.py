#!/usr/bin/env python3
"""
Unpin Slack Message

Unpin a message using pins.remove.

Usage:
    python unpin_message.py --channel C123 --timestamp 1234567890.123456
    python unpin_message.py --channel C123 --timestamp 1234567890.123456 --yes
    python unpin_message.py --channel C123 --timestamp 1234567890.123456 --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def unpin_message(channel, timestamp):
    """Unpin a message"""
    client = get_client()

    data = {
        'channel': channel,
        'timestamp': timestamp
    }

    return client.post('pins.remove', data)


def main():
    parser = argparse.ArgumentParser(description='Unpin a Slack message')
    parser.add_argument('--channel', '-c', required=True,
                        help='Channel ID')
    parser.add_argument('--timestamp', '--ts', required=True,
                        help='Message timestamp')
    parser.add_argument('--yes', '-y', action='store_true',
                        help='Skip confirmation prompt')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        # Confirmation prompt unless --yes flag is provided
        if not args.yes and not args.json:
            print(f"\n[!] WARNING: This will unpin the message.")
            print(f"    Channel: {args.channel}")
            print(f"    Timestamp: {args.timestamp}")
            confirm = input("\n    Type 'unpin' to confirm: ")
            if confirm.lower() != 'unpin':
                print("\n[X] Aborted. Message was NOT unpinned.\n")
                sys.exit(0)

        result = unpin_message(
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
            print(f"\n[OK] Message unpinned!")
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
            print(f"\n[X] Failed to unpin message: {e}")
            print(f"    {explain_error(e.error_code)}")

            if e.error_code == 'no_pin':
                print("    Hint: This message is not pinned.")
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
