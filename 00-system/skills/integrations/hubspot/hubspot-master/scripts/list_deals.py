#!/usr/bin/env python3
"""
List HubSpot Deals

Retrieves deals from HubSpot CRM with pagination support.

Usage:
    python list_deals.py [--limit N] [--properties PROPS] [--after CURSOR] [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from hubspot_client import get_client, HubSpotError


def list_deals(limit=10, properties=None, after=None):
    """List deals from HubSpot."""
    client = get_client()

    if properties is None:
        properties = ['dealname', 'amount', 'dealstage', 'pipeline', 'closedate', 'hubspot_owner_id']

    params = {
        'limit': min(limit, 100),
        'properties': ','.join(properties) if isinstance(properties, list) else properties
    }

    if after:
        params['after'] = after

    return client.get('/crm/v3/objects/deals', params=params)


def main():
    parser = argparse.ArgumentParser(description='List HubSpot deals')
    parser.add_argument('--limit', type=int, default=10, help='Number of results (max 100)')
    parser.add_argument('--properties', type=str, default='dealname,amount,dealstage,pipeline,closedate',
                       help='Comma-separated property names')
    parser.add_argument('--after', type=str, help='Pagination cursor')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        properties = args.properties.split(',') if args.properties else None
        result = list_deals(args.limit, properties, args.after)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            deals = result.get('results', [])
            print(f"\nFound {len(deals)} deals:\n")

            for i, deal in enumerate(deals, 1):
                props = deal.get('properties', {})
                name = props.get('dealname', 'No name')
                amount = props.get('amount', '0')
                stage = props.get('dealstage', 'Unknown')

                print(f"{i}. {name}")
                print(f"   ID: {deal.get('id')}")
                print(f"   Amount: ${amount}")
                print(f"   Stage: {stage}")
                if props.get('closedate'):
                    print(f"   Close Date: {props.get('closedate')}")
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
