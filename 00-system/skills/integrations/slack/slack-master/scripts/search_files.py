#!/usr/bin/env python3
"""
Search Slack Files

Search files using search.files.

Usage:
    python search_files.py --query "report.pdf"
    python search_files.py --query "from:@john" --count 50
    python search_files.py --query "type:pdf" --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def search_files(query, count=20, page=1, sort='timestamp', sort_dir='desc'):
    """Search files"""
    client = get_client()

    params = {
        'query': query,
        'count': min(count, 100),
        'page': page,
        'sort': sort,
        'sort_dir': sort_dir
    }

    result = client.get('search.files', params)
    return result.get('files', {})


def main():
    parser = argparse.ArgumentParser(description='Search Slack files')
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
        result = search_files(
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
                'files': [{
                    'id': f.get('id'),
                    'name': f.get('name'),
                    'title': f.get('title'),
                    'filetype': f.get('filetype'),
                    'mimetype': f.get('mimetype'),
                    'size': f.get('size'),
                    'user': f.get('user'),
                    'created': f.get('created'),
                    'permalink': f.get('permalink'),
                    'url_private': f.get('url_private')
                } for f in matches]
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"\n{'='*60}")
            print(f"File Search: \"{args.query}\"")
            print(f"Found {total} files (showing page {paging.get('page', 1)} of {paging.get('pages', 1)})")
            print(f"{'='*60}\n")

            from datetime import datetime

            for f in matches:
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

                print(f"  [{filetype}] {name} ({size_str})")
                print(f"       Created: {created}")
                if f.get('permalink'):
                    print(f"       Link: {f['permalink']}")
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
