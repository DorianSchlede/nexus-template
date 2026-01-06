#!/usr/bin/env python3
"""
Search HubSpot Deals

Searches deals in HubSpot CRM by various criteria.

Usage:
    python search_deals.py [--name NAME] [--stage STAGE] [--min-amount N] [--max-amount N] [--limit N] [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from hubspot_client import get_client, HubSpotError


def search_deals(name=None, stage=None, min_amount=None, max_amount=None, limit=10):
    """Search deals in HubSpot."""
    client = get_client()

    filters = []

    if name:
        filters.append({
            'propertyName': 'dealname',
            'operator': 'CONTAINS_TOKEN',
            'value': name
        })

    if stage:
        filters.append({
            'propertyName': 'dealstage',
            'operator': 'EQ',
            'value': stage
        })

    if min_amount is not None:
        filters.append({
            'propertyName': 'amount',
            'operator': 'GTE',
            'value': str(min_amount)
        })

    if max_amount is not None:
        filters.append({
            'propertyName': 'amount',
            'operator': 'LTE',
            'value': str(max_amount)
        })

    if not filters:
        return client.get('/crm/v3/objects/deals', params={
            'limit': limit,
            'properties': 'dealname,amount,dealstage,pipeline,closedate'
        })

    search_body = {
        'filterGroups': [{'filters': filters}],
        'properties': ['dealname', 'amount', 'dealstage', 'pipeline', 'closedate'],
        'limit': limit
    }

    return client.post('/crm/v3/objects/deals/search', search_body)


def main():
    parser = argparse.ArgumentParser(description='Search HubSpot deals')
    parser.add_argument('--name', type=str, help='Search by deal name')
    parser.add_argument('--stage', type=str, help='Filter by deal stage')
    parser.add_argument('--min-amount', type=float, help='Minimum deal amount')
    parser.add_argument('--max-amount', type=float, help='Maximum deal amount')
    parser.add_argument('--limit', type=int, default=10, help='Max results')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = search_deals(
            name=args.name,
            stage=args.stage,
            min_amount=args.min_amount,
            max_amount=args.max_amount,
            limit=args.limit
        )

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            deals = result.get('results', [])
            total = result.get('total', len(deals))

            if not deals:
                print("\nNo deals found matching your criteria.")
            else:
                print(f"\nFound {total} deal(s):\n")

                for i, deal in enumerate(deals, 1):
                    props = deal.get('properties', {})
                    print(f"{i}. {props.get('dealname', 'No name')}")
                    print(f"   ID: {deal.get('id')}")
                    if props.get('amount'):
                        print(f"   Amount: ${props.get('amount')}")
                    print(f"   Stage: {props.get('dealstage', 'Unknown')}")
                    print()

    except HubSpotError as e:
        if args.json:
            print(json.dumps({'error': True, 'status_code': e.status_code, 'message': e.message}, indent=2))
        else:
            print(f"\n[ERROR] {e.message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
