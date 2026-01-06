#!/usr/bin/env python3
"""
List Slack Pins

List pinned items in a channel using pins.list.

Usage:
    python list_pins.py --channel C123
    python list_pins.py --channel C123 --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def list_pins(channel):
    """List pinned items"""
    client = get_client()

    params = {'channel': channel}
    result = client.get('pins.list', params)
    return result.get('items', [])


def main():
    parser = argparse.ArgumentParser(description='List pinned Slack messages')
    parser.add_argument('--channel', '-c', required=True,
                        help='Channel ID')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        pins = list_pins(args.channel)

        if args.json:
            output = {
                'success': True,
                'channel': args.channel,
                'count': len(pins),
                'pins': [{
                    'type': p.get('type'),
                    'created': p.get('created'),
                    'created_by': p.get('created_by'),
                    'message': {
                        'ts': p.get('message', {}).get('ts'),
                        'text': p.get('message', {}).get('text'),
                        'user': p.get('message', {}).get('user'),
                        'permalink': p.get('message', {}).get('permalink')
                    } if p.get('message') else None
                } for p in pins]
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"\n{'='*60}")
            print(f"Pinned Items ({len(pins)} found)")
            print(f"{'='*60}\n")

            from datetime import datetime

            if pins:
                for p in pins:
                    pin_type = p.get('type', 'unknown')
                    created = datetime.fromtimestamp(p.get('created', 0)).strftime('%Y-%m-%d')
                    pinned_by = p.get('created_by', 'unknown')

                    if pin_type == 'message' and p.get('message'):
                        msg = p['message']
                        text = msg.get('text', '')[:80]
                        user = msg.get('user', 'unknown')
                        ts = msg.get('ts', '')

                        print(f"  Message by {user}:")
                        print(f"    \"{text}{'...' if len(msg.get('text', '')) > 80 else ''}\"")
                        print(f"    Pinned: {created} by {pinned_by}")
                        print(f"    TS: {ts}")
                        print()
                    else:
                        print(f"  [{pin_type}] Pinned: {created}")
                        print()
            else:
                print("No pinned items in this channel.")
                print()

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Failed to list pins: {e}")
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
