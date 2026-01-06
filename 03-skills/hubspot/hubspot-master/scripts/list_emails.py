#!/usr/bin/env python3
"""
List HubSpot Email Engagements

Retrieves email engagement history from HubSpot.

Usage:
    python list_emails.py [--limit N] [--after CURSOR] [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from hubspot_client import get_client, HubSpotError


def list_emails(limit=10, after=None):
    """List email engagements from HubSpot."""
    client = get_client()

    params = {
        'limit': min(limit, 100),
        'properties': 'hs_email_subject,hs_email_text,hs_email_direction,hs_timestamp,hs_email_status'
    }

    if after:
        params['after'] = after

    return client.get('/crm/v3/objects/emails', params=params)


def main():
    parser = argparse.ArgumentParser(description='List HubSpot email engagements')
    parser.add_argument('--limit', type=int, default=10, help='Number of results')
    parser.add_argument('--after', type=str, help='Pagination cursor')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = list_emails(args.limit, args.after)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            emails = result.get('results', [])
            print(f"\nFound {len(emails)} email engagements:\n")

            for i, email in enumerate(emails, 1):
                props = email.get('properties', {})
                subject = props.get('hs_email_subject', 'No subject')
                direction = props.get('hs_email_direction', 'Unknown')
                timestamp = props.get('hs_timestamp', '')

                print(f"{i}. {subject}")
                print(f"   ID: {email.get('id')}")
                print(f"   Direction: {direction}")
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
