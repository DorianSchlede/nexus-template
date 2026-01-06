#!/usr/bin/env python3
"""
Schedule Slack Message

Schedule a message for later using chat.scheduleMessage.

Usage:
    python schedule_message.py --channel C123 --text "Hello!" --post-at 1735689600
    python schedule_message.py --channel C123 --text "Hello!" --post-at 1735689600 --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def schedule_message(channel, text, post_at, thread_ts=None):
    """Schedule a message for later"""
    client = get_client()

    data = {
        'channel': channel,
        'text': text,
        'post_at': post_at
    }

    if thread_ts:
        data['thread_ts'] = thread_ts

    return client.post('chat.scheduleMessage', data)


def main():
    parser = argparse.ArgumentParser(description='Schedule a Slack message')
    parser.add_argument('--channel', '-c', required=True,
                        help='Channel ID')
    parser.add_argument('--text', '-t', required=True,
                        help='Message text')
    parser.add_argument('--post-at', required=True, type=int,
                        help='Unix timestamp when to post')
    parser.add_argument('--thread-ts',
                        help='Thread timestamp to reply to')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview scheduled message without scheduling')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        # Dry-run mode
        if args.dry_run:
            from datetime import datetime
            post_time = datetime.fromtimestamp(args.post_at)
            if args.json:
                output = {
                    'dry_run': True,
                    'would_schedule': {
                        'channel': args.channel,
                        'text': args.text,
                        'post_at': args.post_at,
                        'post_at_formatted': post_time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                }
                print(json.dumps(output, indent=2))
            else:
                print(f"\n[DRY-RUN] Message would be scheduled (not actually scheduled):")
                print(f"    Channel: {args.channel}")
                print(f"    Text: {args.text}")
                print(f"    Scheduled for: {post_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print()
            sys.exit(0)

        result = schedule_message(
            channel=args.channel,
            text=args.text,
            post_at=args.post_at,
            thread_ts=args.thread_ts
        )

        if args.json:
            output = {
                'success': True,
                'scheduled_message_id': result.get('scheduled_message_id'),
                'channel': result.get('channel'),
                'post_at': result.get('post_at')
            }
            print(json.dumps(output, indent=2))
        else:
            from datetime import datetime
            post_time = datetime.fromtimestamp(result.get('post_at', args.post_at))
            print(f"\n[OK] Message scheduled!")
            print(f"    Channel: {result.get('channel')}")
            print(f"    Scheduled for: {post_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"    Message ID: {result.get('scheduled_message_id')}")
            print()

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Failed to schedule message: {e}")
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
