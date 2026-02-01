#!/usr/bin/env python3
"""
Create HubSpot Meeting Engagement

Logs a meeting engagement to HubSpot.

Usage:
    python create_meeting.py --title TITLE [--body BODY] [--start START] [--end END] [--json]
"""

import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from hubspot_client import get_client, HubSpotError


def create_meeting(title, body=None, start_time=None, end_time=None):
    """
    Create a meeting engagement in HubSpot.

    Args:
        title: Meeting title
        body: Meeting notes/body
        start_time: ISO start timestamp
        end_time: ISO end timestamp

    Returns:
        dict with created meeting data
    """
    client = get_client()

    now = datetime.utcnow()
    if start_time is None:
        start_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    if end_time is None:
        end_time = (now + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%SZ')

    properties = {
        'hs_timestamp': start_time,
        'hs_meeting_title': title,
        'hs_meeting_start_time': start_time,
        'hs_meeting_end_time': end_time
    }

    if body:
        properties['hs_meeting_body'] = body

    return client.post('/crm/v3/objects/meetings', {'properties': properties})


def main():
    parser = argparse.ArgumentParser(description='Create HubSpot meeting engagement')
    parser.add_argument('--title', type=str, required=True, help='Meeting title')
    parser.add_argument('--body', type=str, help='Meeting notes/body')
    parser.add_argument('--start', type=str, help='Start time (ISO format)')
    parser.add_argument('--end', type=str, help='End time (ISO format)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = create_meeting(
            title=args.title,
            body=args.body,
            start_time=args.start,
            end_time=args.end
        )

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            props = result.get('properties', {})
            print(f"\n[SUCCESS] Meeting created!")
            print(f"  ID: {result.get('id')}")
            print(f"  Title: {props.get('hs_meeting_title')}")
            if props.get('hs_meeting_start_time'):
                print(f"  Start: {props.get('hs_meeting_start_time')}")
            if props.get('hs_meeting_end_time'):
                print(f"  End: {props.get('hs_meeting_end_time')}")
            print()

    except HubSpotError as e:
        if args.json:
            print(json.dumps({'error': True, 'status_code': e.status_code, 'message': e.message}, indent=2))
        else:
            print(f"\n[ERROR] {e.message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
