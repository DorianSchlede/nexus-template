#!/usr/bin/env python3
"""
Update Slack Message

Update an existing message using chat.update.

Usage:
    python update_message.py --channel C123 --ts 1234567890.123456 --text "Updated text"
    python update_message.py --channel C123 --ts 1234567890.123456 --text "Updated" --dry-run
    python update_message.py --channel C123 --ts 1234567890.123456 --text "Updated" --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def update_message(channel, ts, text):
    """Update an existing message"""
    client = get_client()

    data = {
        'channel': channel,
        'ts': ts,
        'text': text
    }

    return client.post('chat.update', data)


def main():
    parser = argparse.ArgumentParser(description='Update a Slack message')
    parser.add_argument('--channel', '-c', required=True,
                        help='Channel ID')
    parser.add_argument('--ts', required=True,
                        help='Timestamp of message to update')
    parser.add_argument('--text', '-t', required=True,
                        help='New message text')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview update without applying')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        # Dry-run mode - show what would be updated without actually updating
        if args.dry_run:
            if args.json:
                output = {
                    'dry_run': True,
                    'would_update': {
                        'channel': args.channel,
                        'ts': args.ts,
                        'new_text': args.text
                    }
                }
                print(json.dumps(output, indent=2))
            else:
                print(f"\n[DRY-RUN] Message would be updated (not actually updated):")
                print(f"    Channel: {args.channel}")
                print(f"    Timestamp: {args.ts}")
                print(f"    New text: {args.text}")
                print()
            sys.exit(0)

        result = update_message(
            channel=args.channel,
            ts=args.ts,
            text=args.text
        )

        if args.json:
            output = {
                'success': True,
                'channel': result.get('channel'),
                'ts': result.get('ts'),
                'text': result.get('text')
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"\n[OK] Message updated!")
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
            print(f"\n[X] Failed to update message: {e}")
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
