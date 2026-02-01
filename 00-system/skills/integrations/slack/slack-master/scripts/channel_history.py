#!/usr/bin/env python3
"""
Get Slack Channel History

Get messages from a channel using conversations.history.

Usage:
    python channel_history.py --channel C123
    python channel_history.py --channel C123 --limit 50
    python channel_history.py --channel C123 --oldest 1234567890.000000 --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def get_channel_history(channel, limit=20, oldest=None, latest=None, inclusive=False):
    """Get messages from a channel"""
    client = get_client()

    params = {
        'channel': channel,
        'limit': min(limit, 1000)
    }

    if oldest:
        params['oldest'] = oldest
    if latest:
        params['latest'] = latest
    if inclusive:
        params['inclusive'] = True

    result = client.get('conversations.history', params)
    return result.get('messages', []), result.get('has_more', False)


def main():
    parser = argparse.ArgumentParser(description='Get Slack channel history')
    parser.add_argument('--channel', '-c', required=True,
                        help='Channel ID')
    parser.add_argument('--limit', '-l', type=int, default=20,
                        help='Number of messages to retrieve')
    parser.add_argument('--oldest',
                        help='Start of time range (timestamp)')
    parser.add_argument('--latest',
                        help='End of time range (timestamp)')
    parser.add_argument('--inclusive', action='store_true',
                        help='Include messages at oldest/latest timestamps')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        messages, has_more = get_channel_history(
            channel=args.channel,
            limit=args.limit,
            oldest=args.oldest,
            latest=args.latest,
            inclusive=args.inclusive
        )

        if args.json:
            output = {
                'success': True,
                'channel': args.channel,
                'count': len(messages),
                'has_more': has_more,
                'messages': [{
                    'ts': msg.get('ts'),
                    'user': msg.get('user'),
                    'text': msg.get('text'),
                    'type': msg.get('type'),
                    'subtype': msg.get('subtype'),
                    'thread_ts': msg.get('thread_ts'),
                    'reply_count': msg.get('reply_count', 0),
                    'reactions': msg.get('reactions', [])
                } for msg in messages]
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"\n{'='*60}")
            print(f"Channel History ({len(messages)} messages)")
            print(f"{'='*60}\n")

            from datetime import datetime

            for msg in reversed(messages):  # Show oldest first
                ts = float(msg.get('ts', 0))
                time_str = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')
                user = msg.get('user', 'unknown')
                text = msg.get('text', '')[:100]  # Truncate long messages

                # Handle different message types
                subtype = msg.get('subtype', '')
                if subtype:
                    print(f"[{time_str}] ({subtype}) {text}")
                else:
                    print(f"[{time_str}] {user}: {text}")

                # Show thread info
                if msg.get('reply_count'):
                    print(f"           +-- {msg['reply_count']} replies")

            if has_more:
                print(f"\n... more messages available (use --oldest to paginate)")
            print()

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Failed to get channel history: {e}")
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
