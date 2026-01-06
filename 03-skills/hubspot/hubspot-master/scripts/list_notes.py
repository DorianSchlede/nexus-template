#!/usr/bin/env python3
"""
List HubSpot Notes

Retrieves notes from HubSpot.

Usage:
    python list_notes.py [--limit N] [--after CURSOR] [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from hubspot_client import get_client, HubSpotError


def list_notes(limit=10, after=None):
    """List notes from HubSpot."""
    client = get_client()

    params = {
        'limit': min(limit, 100),
        'properties': 'hs_note_body,hs_timestamp'
    }

    if after:
        params['after'] = after

    return client.get('/crm/v3/objects/notes', params=params)


def main():
    parser = argparse.ArgumentParser(description='List HubSpot notes')
    parser.add_argument('--limit', type=int, default=10, help='Number of results')
    parser.add_argument('--after', type=str, help='Pagination cursor')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = list_notes(args.limit, args.after)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            notes = result.get('results', [])
            print(f"\nFound {len(notes)} notes:\n")

            for i, note in enumerate(notes, 1):
                props = note.get('properties', {})
                body = props.get('hs_note_body', 'No content')
                timestamp = props.get('hs_timestamp', '')

                # Truncate long notes
                if len(body) > 100:
                    body = body[:100] + '...'

                print(f"{i}. {body}")
                print(f"   ID: {note.get('id')}")
                if timestamp:
                    print(f"   Date: {timestamp}")
                print()

            paging = result.get('paging', {})
            if paging.get('next'):
                print(f"More results available. Use --after {paging['next']['after']}")

    except HubSpotError as e:
        if args.json:
            print(json.dumps({'error': True, 'status_code': e.status_code, 'message': e.message}, indent=2))
        else:
            print(f"Error: {e.message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
