#!/usr/bin/env python3
"""
Create HubSpot Deal

Creates a new deal in HubSpot CRM.

Usage:
    python create_deal.py --name NAME [--amount AMOUNT] [--stage STAGE] [--pipeline PIPELINE] [--closedate DATE] [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from hubspot_client import get_client, HubSpotError


def create_deal(name, amount=None, stage=None, pipeline=None, closedate=None, **extra_properties):
    """Create a new deal in HubSpot."""
    client = get_client()

    properties = {'dealname': name}

    if amount is not None:
        properties['amount'] = str(amount)
    if stage:
        properties['dealstage'] = stage
    if pipeline:
        properties['pipeline'] = pipeline
    if closedate:
        properties['closedate'] = closedate

    properties.update(extra_properties)

    return client.post('/crm/v3/objects/deals', {'properties': properties})


def main():
    parser = argparse.ArgumentParser(description='Create HubSpot deal')
    parser.add_argument('--name', type=str, required=True, help='Deal name (required)')
    parser.add_argument('--amount', type=float, help='Deal amount')
    parser.add_argument('--stage', type=str, help='Deal stage (e.g., qualifiedtobuy, presentationscheduled, closedwon)')
    parser.add_argument('--pipeline', type=str, default='default', help='Pipeline (default: default)')
    parser.add_argument('--closedate', type=str, help='Close date (YYYY-MM-DD)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = create_deal(
            name=args.name,
            amount=args.amount,
            stage=args.stage,
            pipeline=args.pipeline,
            closedate=args.closedate
        )

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            props = result.get('properties', {})
            print(f"\n[SUCCESS] Deal created!")
            print(f"  ID: {result.get('id')}")
            print(f"  Name: {props.get('dealname')}")
            if props.get('amount'):
                print(f"  Amount: ${props.get('amount')}")
            if props.get('dealstage'):
                print(f"  Stage: {props.get('dealstage')}")
            print()

    except HubSpotError as e:
        if args.json:
            print(json.dumps({'error': True, 'status_code': e.status_code, 'message': e.message, 'category': e.category}, indent=2))
        else:
            print(f"\n[ERROR] {e.message}")
            if e.category == 'VALIDATION_ERROR':
                for error in e.errors:
                    print(f"  - {error.get('name', 'Field')}: {error.get('message', 'Invalid')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
