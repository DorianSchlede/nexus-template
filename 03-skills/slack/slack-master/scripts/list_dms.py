#!/usr/bin/env python3
"""
List Slack Direct Messages

List DM conversations using conversations.list with type=im.

Usage:
    python list_dms.py
    python list_dms.py --limit 50
    python list_dms.py --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def list_dms(limit=100):
    """List DM conversations"""
    client = get_client()

    params = {
        'types': 'im',
        'limit': min(limit, 1000)
    }

    if limit > 200:
        return client.paginate('conversations.list', params, limit)
    else:
        result = client.get('conversations.list', params)
        return result.get('channels', [])


def get_user_info(client, user_id):
    """Get user info for a DM"""
    try:
        result = client.get('users.info', {'user': user_id})
        return result.get('user', {})
    except:
        return {}


def main():
    parser = argparse.ArgumentParser(description='List Slack DM conversations')
    parser.add_argument('--limit', '-l', type=int, default=100,
                        help='Maximum DMs to return')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        client = get_client()
        dms = list_dms(limit=args.limit)

        # Enrich with user info
        enriched_dms = []
        for dm in dms:
            user_id = dm.get('user')
            user_info = get_user_info(client, user_id) if user_id else {}
            enriched_dms.append({
                'channel_id': dm.get('id'),
                'user_id': user_id,
                'user_name': user_info.get('name'),
                'real_name': user_info.get('real_name'),
                'is_open': dm.get('is_open', False)
            })

        if args.json:
            output = {
                'success': True,
                'count': len(enriched_dms),
                'dms': enriched_dms
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"\n{'='*60}")
            print(f"Direct Messages ({len(enriched_dms)} found)")
            print(f"{'='*60}\n")

            for dm in enriched_dms:
                name = dm['real_name'] or dm['user_name'] or 'Unknown'
                username = dm['user_name'] or ''
                status = '(open)' if dm['is_open'] else ''

                print(f"  {name} (@{username}) - {dm['channel_id']} {status}")

            print()

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Failed to list DMs: {e}")
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
