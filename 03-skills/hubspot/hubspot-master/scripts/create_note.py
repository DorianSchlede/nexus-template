#!/usr/bin/env python3
"""
Create HubSpot Note

Creates a note in HubSpot.

Usage:
    python create_note.py --body BODY [--timestamp TIMESTAMP] [--json]
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from hubspot_client import get_client, HubSpotError


def create_note(body, timestamp=None):
    """
    Create a note in HubSpot.

    Args:
        body: Note content
        timestamp: ISO timestamp (default: now)

    Returns:
        dict with created note data
    """
    client = get_client()

    if timestamp is None:
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    properties = {
        'hs_timestamp': timestamp,
        'hs_note_body': body
    }

    return client.post('/crm/v3/objects/notes', {'properties': properties})


def main():
    parser = argparse.ArgumentParser(description='Create HubSpot note')
    parser.add_argument('--body', type=str, required=True, help='Note content')
    parser.add_argument('--timestamp', type=str, help='ISO timestamp (default: now)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = create_note(
            body=args.body,
            timestamp=args.timestamp
        )

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            props = result.get('properties', {})
            body = props.get('hs_note_body', '')
            if len(body) > 50:
                body = body[:50] + '...'

            print(f"\n[SUCCESS] Note created!")
            print(f"  ID: {result.get('id')}")
            print(f"  Content: {body}")
            print()

    except HubSpotError as e:
        if args.json:
            print(json.dumps({'error': True, 'status_code': e.status_code, 'message': e.message}, indent=2))
        else:
            print(f"\n[ERROR] {e.message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
