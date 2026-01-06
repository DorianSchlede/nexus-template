#!/usr/bin/env python3
"""
Search Slack Messages

Search messages using search.messages.

Usage:
    python search_messages.py --query "project update"
    python search_messages.py --query "from:@john in:#general" --count 50
    python search_messages.py --query "has:link after:2024-01-01" --json

Search modifiers:
    from:@user      - From specific user
    in:#channel     - In specific channel
    before:date     - Before date (YYYY-MM-DD)
    after:date      - After date
    has:link        - Contains links
    has:reaction    - Has reactions
    has:star        - Is starred
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def search_messages(query, count=20, page=1, sort='timestamp', sort_dir='desc'):
    """Search messages"""
    client = get_client()

    params = {
        'query': query,
        'count': min(count, 100),
        'page': page,
        'sort': sort,
        'sort_dir': sort_dir
    }

    result = client.get('search.messages', params)
    return result.get('messages', {})


def main():
    parser = argparse.ArgumentParser(description='Search Slack messages')
    parser.add_argument('--query', '-q', required=True,
                        help='Search query')
    parser.add_argument('--count', '-c', type=int, default=20,
                        help='Number of results (max 100)')
    parser.add_argument('--page', '-p', type=int, default=1,
                        help='Page number')
    parser.add_argument('--sort', choices=['score', 'timestamp'], default='timestamp',
                        help='Sort by relevance or time')
    parser.add_argument('--sort-dir', choices=['asc', 'desc'], default='desc',
                        help='Sort direction')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        result = search_messages(
            query=args.query,
            count=args.count,
            page=args.page,
            sort=args.sort,
            sort_dir=args.sort_dir
        )

        matches = result.get('matches', [])
        total = result.get('total', 0)
        paging = result.get('paging', {})

        if args.json:
            output = {
                'success': True,
                'query': args.query,
                'total': total,
                'page': paging.get('page', 1),
                'pages': paging.get('pages', 1),
                'count': len(matches),
                'messages': [{
                    'ts': m.get('ts'),
                    'text': m.get('text'),
                    'user': m.get('user'),
                    'username': m.get('username'),
                    'channel': m.get('channel', {}).get('id'),
                    'channel_name': m.get('channel', {}).get('name'),
                    'permalink': m.get('permalink')
                } for m in matches]
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"\n{'='*60}")
            print(f"Search Results: \"{args.query}\"")
            print(f"Found {total} messages (showing page {paging.get('page', 1)} of {paging.get('pages', 1)})")
            print(f"{'='*60}\n")

            from datetime import datetime

            for msg in matches:
                ts = float(msg.get('ts', 0))
                time_str = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')
                channel = msg.get('channel', {}).get('name', 'unknown')
                user = msg.get('username', msg.get('user', 'unknown'))
                text = msg.get('text', '')[:150]  # Truncate

                print(f"[{time_str}] #{channel}")
                print(f"  @{user}: {text}")
                if msg.get('permalink'):
                    print(f"  Link: {msg['permalink']}")
                print()

            if paging.get('pages', 1) > paging.get('page', 1):
                print(f"More results available. Use --page {paging.get('page', 1) + 1} to see next page.")

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Search failed: {e}")
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
