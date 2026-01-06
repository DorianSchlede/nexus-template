#!/usr/bin/env python3
"""
List Slack Files

List files using files.list.

Usage:
    python list_files.py
    python list_files.py --channel C123
    python list_files.py --user U123 --types images
    python list_files.py --limit 50 --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def list_files(channel=None, user=None, types=None, count=20, page=1):
    """List files"""
    client = get_client()

    params = {
        'count': min(count, 100),
        'page': page
    }

    if channel:
        params['channel'] = channel
    if user:
        params['user'] = user
    if types:
        params['types'] = types

    result = client.get('files.list', params)
    return result.get('files', []), result.get('paging', {})


def main():
    parser = argparse.ArgumentParser(description='List Slack files')
    parser.add_argument('--channel', '-c',
                        help='Filter by channel ID')
    parser.add_argument('--user', '-u',
                        help='Filter by user ID')
    parser.add_argument('--types', '-t',
                        help='Filter by type: all, spaces, snippets, images, gdocs, zips, pdfs')
    parser.add_argument('--limit', '-l', type=int, default=20,
                        help='Number of results')
    parser.add_argument('--page', '-p', type=int, default=1,
                        help='Page number')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        files, paging = list_files(
            channel=args.channel,
            user=args.user,
            types=args.types,
            count=args.limit,
            page=args.page
        )

        if args.json:
            output = {
                'success': True,
                'count': len(files),
                'total': paging.get('total', len(files)),
                'page': paging.get('page', 1),
                'pages': paging.get('pages', 1),
                'files': [{
                    'id': f.get('id'),
                    'name': f.get('name'),
                    'title': f.get('title'),
                    'filetype': f.get('filetype'),
                    'mimetype': f.get('mimetype'),
                    'size': f.get('size'),
                    'user': f.get('user'),
                    'created': f.get('created'),
                    'permalink': f.get('permalink')
                } for f in files]
            }
            print(json.dumps(output, indent=2))
        else:
            total = paging.get('total', len(files))
            print(f"\n{'='*60}")
            print(f"Files ({len(files)} of {total})")
            print(f"{'='*60}\n")

            from datetime import datetime

            for f in files:
                created = datetime.fromtimestamp(f.get('created', 0)).strftime('%Y-%m-%d')
                name = f.get('name', 'Untitled')
                filetype = f.get('filetype', 'unknown')
                size_bytes = f.get('size', 0)

                # Format size
                if size_bytes > 1024 * 1024:
                    size_str = f"{size_bytes / (1024*1024):.1f} MB"
                elif size_bytes > 1024:
                    size_str = f"{size_bytes / 1024:.1f} KB"
                else:
                    size_str = f"{size_bytes} bytes"

                print(f"  [{filetype}] {name}")
                print(f"       ID: {f.get('id')}")
                print(f"       Size: {size_str} | Created: {created}")
                print()

            if paging.get('pages', 1) > paging.get('page', 1):
                print(f"More files available. Use --page {paging.get('page', 1) + 1} to see next page.")

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Failed to list files: {e}")
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
