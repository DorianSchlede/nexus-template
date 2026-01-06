#!/usr/bin/env python3
"""
List HubSpot Call Engagements

Retrieves call engagement history from HubSpot.

Usage:
    python list_calls.py [--limit N] [--after CURSOR] [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from hubspot_client import get_client, HubSpotError


def list_calls(limit=10, after=None):
    """List call engagements from HubSpot."""
    client = get_client()

    params = {
        'limit': min(limit, 100),
        'properties': 'hs_call_title,hs_call_body,hs_call_duration,hs_timestamp,hs_call_status'
    }

    if after:
        params['after'] = after

    return client.get('/crm/v3/objects/calls', params=params)


def main():
    parser = argparse.ArgumentParser(description='List HubSpot call engagements')
    parser.add_argument('--limit', type=int, default=10, help='Number of results')
    parser.add_argument('--after', type=str, help='Pagination cursor')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = list_calls(args.limit, args.after)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            calls = result.get('results', [])
            print(f"\nFound {len(calls)} call engagements:\n")

            for i, call in enumerate(calls, 1):
                props = call.get('properties', {})
                title = props.get('hs_call_title', 'No title')
                duration = props.get('hs_call_duration', '0')
                timestamp = props.get('hs_timestamp', '')

                # Convert duration from ms to minutes
                try:
                    duration_min = int(duration) // 60000
                except:
                    duration_min = 0

                print(f"{i}. {title}")
                print(f"   ID: {call.get('id')}")
                print(f"   Duration: {duration_min} minutes")
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
