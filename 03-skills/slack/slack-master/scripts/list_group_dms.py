#!/usr/bin/env python3
"""
List Slack Group Direct Messages

List group DM (multi-party IM) conversations using conversations.list with type=mpim.

Usage:
    python list_group_dms.py
    python list_group_dms.py --limit 50
    python list_group_dms.py --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def list_group_dms(limit=100):
    """List group DM conversations"""
    client = get_client()

    params = {
        'types': 'mpim',
        'limit': min(limit, 1000)
    }

    if limit > 200:
        return client.paginate('conversations.list', params, limit)
    else:
        result = client.get('conversations.list', params)
        return result.get('channels', [])


def main():
    parser = argparse.ArgumentParser(description='List Slack group DM conversations')
    parser.add_argument('--limit', '-l', type=int, default=100,
                        help='Maximum group DMs to return')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        client = get_client()
        group_dms = list_group_dms(limit=args.limit)

        if args.json:
            output = {
                'success': True,
                'count': len(group_dms),
                'group_dms': [{
                    'channel_id': gd.get('id'),
                    'name': gd.get('name'),
                    'purpose': gd.get('purpose', {}).get('value', ''),
                    'num_members': gd.get('num_members', 0),
                    'is_open': gd.get('is_open', False)
                } for gd in group_dms]
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"\n{'='*60}")
            print(f"Group Direct Messages ({len(group_dms)} found)")
            print(f"{'='*60}\n")

            if not group_dms:
                print("  No group DMs found.\n")
            else:
                for gd in group_dms:
                    name = gd.get('name', 'Unnamed')
                    channel_id = gd.get('id')
                    num_members = gd.get('num_members', 0)
                    status = '(open)' if gd.get('is_open') else ''

                    print(f"  {name}")
                    print(f"    ID: {channel_id} | Members: {num_members} {status}")
                    print()

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Failed to list group DMs: {e}")
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
