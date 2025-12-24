#!/usr/bin/env python3
"""
Delete Slack Message

Delete a message using chat.delete.

Usage:
    python delete_message.py --channel C123 --ts 1234567890.123456
    python delete_message.py --channel C123 --ts 1234567890.123456 --yes
    python delete_message.py --channel C123 --ts 1234567890.123456 --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def delete_message(channel, ts):
    """Delete a message"""
    client = get_client()

    data = {
        'channel': channel,
        'ts': ts
    }

    return client.post('chat.delete', data)


def main():
    parser = argparse.ArgumentParser(description='Delete a Slack message')
    parser.add_argument('--channel', '-c', required=True,
                        help='Channel ID')
    parser.add_argument('--ts', required=True,
                        help='Timestamp of message to delete')
    parser.add_argument('--yes', '-y', action='store_true',
                        help='Skip confirmation prompt')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        # Confirmation prompt unless --yes flag is provided
        if not args.yes and not args.json:
            print(f"\n[!] WARNING: This will permanently delete the message.")
            print(f"    Channel: {args.channel}")
            print(f"    Timestamp: {args.ts}")
            confirm = input("\n    Type 'delete' to confirm: ")
            if confirm.lower() != 'delete':
                print("\n[X] Aborted. Message was NOT deleted.\n")
                sys.exit(0)

        result = delete_message(
            channel=args.channel,
            ts=args.ts
        )

        if args.json:
            output = {
                'success': True,
                'channel': result.get('channel'),
                'ts': result.get('ts')
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"\n[OK] Message deleted!")
            print(f"    Channel: {result.get('channel')}")
            print(f"    Timestamp: {result.get('ts')}")
            print()

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Failed to delete message: {e}")
            print(f"    {explain_error(e.error_code)}")
            print()
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
