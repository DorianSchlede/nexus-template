#!/usr/bin/env python3
"""
Leave Slack Channel

Leave a channel using conversations.leave.

Usage:
    python leave_channel.py --channel C123
    python leave_channel.py --channel C123 --yes
    python leave_channel.py --channel C123 --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def leave_channel(channel):
    """Leave a channel"""
    client = get_client()

    data = {'channel': channel}
    return client.post('conversations.leave', data)


def main():
    parser = argparse.ArgumentParser(description='Leave a Slack channel')
    parser.add_argument('--channel', '-c', required=True,
                        help='Channel ID')
    parser.add_argument('--yes', '-y', action='store_true',
                        help='Skip confirmation prompt')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        # Get channel info for better confirmation message
        client = get_client()
        channel_name = args.channel
        try:
            info = client.get('conversations.info', {'channel': args.channel})
            channel_name = f"#{info.get('channel', {}).get('name', args.channel)}"
        except:
            pass

        # Confirmation prompt unless --yes flag is provided
        if not args.yes and not args.json:
            print(f"\n[!] WARNING: You are about to leave {channel_name}")
            confirm = input("\n    Type 'leave' to confirm: ")
            if confirm.lower() != 'leave':
                print("\n[X] Aborted. You did NOT leave the channel.\n")
                sys.exit(0)

        result = leave_channel(args.channel)

        if args.json:
            output = {
                'success': True,
                'channel': args.channel
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"\n[OK] Left channel {args.channel}")
            print()

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Failed to leave channel: {e}")
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
