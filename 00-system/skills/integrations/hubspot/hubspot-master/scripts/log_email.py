#!/usr/bin/env python3
"""
Log HubSpot Email Engagement

Logs an email engagement to HubSpot.

Usage:
    python log_email.py --subject SUBJECT --body BODY [--direction DIRECTION] [--timestamp TIMESTAMP] [--json]
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from hubspot_client import get_client, HubSpotError


def log_email(subject, body, direction='EMAIL', timestamp=None):
    """
    Log an email engagement to HubSpot.

    Args:
        subject: Email subject
        body: Email body content
        direction: EMAIL (sent) or INCOMING_EMAIL
        timestamp: ISO timestamp (default: now)

    Returns:
        dict with created email data
    """
    client = get_client()

    if timestamp is None:
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    properties = {
        'hs_timestamp': timestamp,
        'hs_email_direction': direction,
        'hs_email_subject': subject,
        'hs_email_text': body
    }

    return client.post('/crm/v3/objects/emails', {'properties': properties})


def main():
    parser = argparse.ArgumentParser(description='Log HubSpot email engagement')
    parser.add_argument('--subject', type=str, required=True, help='Email subject')
    parser.add_argument('--body', type=str, required=True, help='Email body content')
    parser.add_argument('--direction', type=str, default='EMAIL',
                       choices=['EMAIL', 'INCOMING_EMAIL'],
                       help='Direction: EMAIL (sent) or INCOMING_EMAIL (received)')
    parser.add_argument('--timestamp', type=str, help='ISO timestamp (default: now)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = log_email(
            subject=args.subject,
            body=args.body,
            direction=args.direction,
            timestamp=args.timestamp
        )

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            props = result.get('properties', {})
            print(f"\n[SUCCESS] Email logged!")
            print(f"  ID: {result.get('id')}")
            print(f"  Subject: {props.get('hs_email_subject')}")
            print(f"  Direction: {props.get('hs_email_direction')}")
            print()

    except HubSpotError as e:
        if args.json:
            print(json.dumps({'error': True, 'status_code': e.status_code, 'message': e.message}, indent=2))
        else:
            print(f"\n[ERROR] {e.message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
