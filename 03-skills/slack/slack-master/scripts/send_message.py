#!/usr/bin/env python3
"""
Send Slack Message

Send a message to a channel or DM using chat.postMessage.

Usage:
    python send_message.py --channel C123 --text "Hello!"
    python send_message.py --channel C123 --text "Reply" --thread-ts 1234567890.123456
    python send_message.py --channel C123 --text "Hello!" --dry-run
    python send_message.py --channel C123 --text "Hello!" --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def send_message(channel, text, thread_ts=None, reply_broadcast=False,
                 unfurl_links=True, unfurl_media=True):
    """Send a message to a channel"""
    client = get_client()

    data = {
        'channel': channel,
        'text': text,
        'unfurl_links': unfurl_links,
        'unfurl_media': unfurl_media
    }

    if thread_ts:
        data['thread_ts'] = thread_ts
        if reply_broadcast:
            data['reply_broadcast'] = True

    return client.post('chat.postMessage', data)


def main():
    parser = argparse.ArgumentParser(description='Send a Slack message')
    parser.add_argument('--channel', '-c', required=True,
                        help='Channel ID or name (e.g., C1234567890 or #general)')
    parser.add_argument('--text', '-t', required=True,
                        help='Message text')
    parser.add_argument('--thread-ts',
                        help='Thread timestamp to reply to')
    parser.add_argument('--reply-broadcast', action='store_true',
                        help='Also post reply to channel')
    parser.add_argument('--no-unfurl-links', action='store_true',
                        help='Disable URL unfurling')
    parser.add_argument('--no-unfurl-media', action='store_true',
                        help='Disable media unfurling')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview message without sending')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        # Dry-run mode - show what would be sent without actually sending
        if args.dry_run:
            if args.json:
                output = {
                    'dry_run': True,
                    'would_send': {
                        'channel': args.channel,
                        'text': args.text,
                        'thread_ts': args.thread_ts,
                        'reply_broadcast': args.reply_broadcast
                    }
                }
                print(json.dumps(output, indent=2))
            else:
                print(f"\n[DRY-RUN] Message would be sent (not actually sent):")
                print(f"    Channel: {args.channel}")
                print(f"    Text: {args.text}")
                if args.thread_ts:
                    print(f"    Thread: {args.thread_ts}")
                print()
            sys.exit(0)

        result = send_message(
            channel=args.channel,
            text=args.text,
            thread_ts=args.thread_ts,
            reply_broadcast=args.reply_broadcast,
            unfurl_links=not args.no_unfurl_links,
            unfurl_media=not args.no_unfurl_media
        )

        if args.json:
            output = {
                'success': True,
                'channel': result.get('channel'),
                'ts': result.get('ts'),
                'message': {
                    'text': result.get('message', {}).get('text'),
                    'user': result.get('message', {}).get('user'),
                    'ts': result.get('message', {}).get('ts')
                }
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"\n[OK] Message sent!")
            print(f"    Channel: {result.get('channel')}")
            print(f"    Timestamp: {result.get('ts')}")
            if args.thread_ts:
                print(f"    Thread: {args.thread_ts}")
            print()

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Failed to send message: {e}")
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
