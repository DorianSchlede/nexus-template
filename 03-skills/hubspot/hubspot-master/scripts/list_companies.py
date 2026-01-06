#!/usr/bin/env python3
"""
List HubSpot Companies

Retrieves companies from HubSpot CRM with pagination support.

Usage:
    python list_companies.py [--limit N] [--properties PROPS] [--after CURSOR] [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from hubspot_client import get_client, HubSpotError


def list_companies(limit=10, properties=None, after=None):
    """List companies from HubSpot."""
    client = get_client()

    if properties is None:
        properties = ['name', 'domain', 'industry', 'phone', 'city', 'numberofemployees']

    params = {
        'limit': min(limit, 100),
        'properties': ','.join(properties) if isinstance(properties, list) else properties
    }

    if after:
        params['after'] = after

    return client.get('/crm/v3/objects/companies', params=params)


def main():
    parser = argparse.ArgumentParser(description='List HubSpot companies')
    parser.add_argument('--limit', type=int, default=10, help='Number of results (max 100)')
    parser.add_argument('--properties', type=str, default='name,domain,industry,phone,city,numberofemployees',
                       help='Comma-separated property names')
    parser.add_argument('--after', type=str, help='Pagination cursor')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        properties = args.properties.split(',') if args.properties else None
        result = list_companies(args.limit, properties, args.after)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            companies = result.get('results', [])
            print(f"\nFound {len(companies)} companies:\n")

            for i, company in enumerate(companies, 1):
                props = company.get('properties', {})
                name = props.get('name', 'No name')
                domain = props.get('domain', '')
                industry = props.get('industry', '')

                print(f"{i}. {name}")
                print(f"   ID: {company.get('id')}")
                if domain:
                    print(f"   Domain: {domain}")
                if industry:
                    print(f"   Industry: {industry}")
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
