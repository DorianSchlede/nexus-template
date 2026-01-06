#!/usr/bin/env python3
"""
Log HubSpot Call Engagement

Logs a call engagement to HubSpot.

Usage:
    python log_call.py --title TITLE [--body BODY] [--duration MINUTES] [--timestamp TIMESTAMP] [--json]
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from hubspot_client import get_client, HubSpotError


def log_call(title, body=None, duration_minutes=None, timestamp=None):
    """
    Log a call engagement to HubSpot.

    Args:
        title: Call title
        body: Call notes/body
        duration_minutes: Call duration in minutes
        timestamp: ISO timestamp (default: now)

    Returns:
        dict with created call data
    """
    client = get_client()

    if timestamp is None:
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    properties = {
        'hs_timestamp': timestamp,
        'hs_call_title': title
    }

    if body:
        properties['hs_call_body'] = body

    if duration_minutes is not None:
        # HubSpot expects duration in milliseconds
        properties['hs_call_duration'] = str(duration_minutes * 60000)

    return client.post('/crm/v3/objects/calls', {'properties': properties})


def main():
    parser = argparse.ArgumentParser(description='Log HubSpot call engagement')
    parser.add_argument('--title', type=str, required=True, help='Call title')
    parser.add_argument('--body', type=str, help='Call notes/body')
    parser.add_argument('--duration', type=int, help='Duration in minutes')
    parser.add_argument('--timestamp', type=str, help='ISO timestamp (default: now)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = log_call(
            title=args.title,
            body=args.body,
            duration_minutes=args.duration,
            timestamp=args.timestamp
        )

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            props = result.get('properties', {})
            print(f"\n[SUCCESS] Call logged!")
            print(f"  ID: {result.get('id')}")
            print(f"  Title: {props.get('hs_call_title')}")
            if props.get('hs_call_duration'):
                duration_min = int(props.get('hs_call_duration', 0)) // 60000
                print(f"  Duration: {duration_min} minutes")
            print()

    except HubSpotError as e:
        if args.json:
            print(json.dumps({'error': True, 'status_code': e.status_code, 'message': e.message}, indent=2))
        else:
            print(f"\n[ERROR] {e.message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
