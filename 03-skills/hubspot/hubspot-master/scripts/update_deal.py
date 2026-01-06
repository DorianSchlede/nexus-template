#!/usr/bin/env python3
"""
Update HubSpot Deal

Updates an existing deal in HubSpot CRM.

Usage:
    python update_deal.py --id DEAL_ID [--name NAME] [--amount AMOUNT] [--stage STAGE] [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from hubspot_client import get_client, HubSpotError


def update_deal(deal_id, name=None, amount=None, stage=None, closedate=None, **extra_properties):
    """Update an existing deal in HubSpot."""
    client = get_client()

    properties = {}

    if name:
        properties['dealname'] = name
    if amount is not None:
        properties['amount'] = str(amount)
    if stage:
        properties['dealstage'] = stage
    if closedate:
        properties['closedate'] = closedate

    properties.update({k: v for k, v in extra_properties.items() if v is not None})

    if not properties:
        raise ValueError("No properties provided to update")

    return client.patch(f'/crm/v3/objects/deals/{deal_id}', {'properties': properties})


def main():
    parser = argparse.ArgumentParser(description='Update HubSpot deal')
    parser.add_argument('--id', type=str, required=True, help='Deal ID to update')
    parser.add_argument('--name', type=str, help='New deal name')
    parser.add_argument('--amount', type=float, help='New amount')
    parser.add_argument('--stage', type=str, help='New deal stage')
    parser.add_argument('--closedate', type=str, help='New close date (YYYY-MM-DD)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = update_deal(
            deal_id=args.id,
            name=args.name,
            amount=args.amount,
            stage=args.stage,
            closedate=args.closedate
        )

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            props = result.get('properties', {})
            print(f"\n[SUCCESS] Deal updated!")
            print(f"  ID: {result.get('id')}")
            print(f"  Name: {props.get('dealname')}")
            if props.get('amount'):
                print(f"  Amount: ${props.get('amount')}")
            if props.get('dealstage'):
                print(f"  Stage: {props.get('dealstage')}")
            print()

    except HubSpotError as e:
        if args.json:
            print(json.dumps({'error': True, 'status_code': e.status_code, 'message': e.message}, indent=2))
        else:
            print(f"\n[ERROR] {e.message}")
            if e.category == 'OBJECT_NOT_FOUND':
                print(f"  Deal with ID {args.id} not found.")
        sys.exit(1)
    except ValueError as e:
        if args.json:
            print(json.dumps({'error': True, 'message': str(e)}, indent=2))
        else:
            print(f"\n[ERROR] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
