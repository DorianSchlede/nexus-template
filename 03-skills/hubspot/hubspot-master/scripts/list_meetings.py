#!/usr/bin/env python3
"""
List HubSpot Meeting Engagements

Retrieves meeting engagement history from HubSpot.

Usage:
    python list_meetings.py [--limit N] [--after CURSOR] [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from hubspot_client import get_client, HubSpotError


def list_meetings(limit=10, after=None):
    """List meeting engagements from HubSpot."""
    client = get_client()

    params = {
        'limit': min(limit, 100),
        'properties': 'hs_meeting_title,hs_meeting_body,hs_meeting_start_time,hs_meeting_end_time,hs_timestamp'
    }

    if after:
        params['after'] = after

    return client.get('/crm/v3/objects/meetings', params=params)


def main():
    parser = argparse.ArgumentParser(description='List HubSpot meeting engagements')
    parser.add_argument('--limit', type=int, default=10, help='Number of results')
    parser.add_argument('--after', type=str, help='Pagination cursor')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = list_meetings(args.limit, args.after)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            meetings = result.get('results', [])
            print(f"\nFound {len(meetings)} meetings:\n")

            for i, meeting in enumerate(meetings, 1):
                props = meeting.get('properties', {})
                title = props.get('hs_meeting_title', 'No title')
                start_time = props.get('hs_meeting_start_time', '')
                end_time = props.get('hs_meeting_end_time', '')

                print(f"{i}. {title}")
                print(f"   ID: {meeting.get('id')}")
                if start_time:
                    print(f"   Start: {start_time}")
                if end_time:
                    print(f"   End: {end_time}")
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
