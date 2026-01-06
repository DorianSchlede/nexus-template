#!/usr/bin/env python3
"""
Search HubSpot Companies

Searches companies in HubSpot CRM by various criteria.

Usage:
    python search_companies.py [--name NAME] [--domain DOMAIN] [--industry INDUSTRY] [--limit N] [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from hubspot_client import get_client, HubSpotError


def search_companies(name=None, domain=None, industry=None, limit=10):
    """Search companies in HubSpot."""
    client = get_client()

    filters = []

    if name:
        filters.append({
            'propertyName': 'name',
            'operator': 'CONTAINS_TOKEN',
            'value': name
        })

    if domain:
        filters.append({
            'propertyName': 'domain',
            'operator': 'CONTAINS_TOKEN',
            'value': domain
        })

    if industry:
        filters.append({
            'propertyName': 'industry',
            'operator': 'EQ',
            'value': industry
        })

    if not filters:
        return client.get('/crm/v3/objects/companies', params={
            'limit': limit,
            'properties': 'name,domain,industry,phone,city'
        })

    search_body = {
        'filterGroups': [{'filters': filters}],
        'properties': ['name', 'domain', 'industry', 'phone', 'city', 'numberofemployees'],
        'limit': limit
    }

    return client.post('/crm/v3/objects/companies/search', search_body)


def main():
    parser = argparse.ArgumentParser(description='Search HubSpot companies')
    parser.add_argument('--name', type=str, help='Search by company name')
    parser.add_argument('--domain', type=str, help='Search by domain')
    parser.add_argument('--industry', type=str, help='Search by industry')
    parser.add_argument('--limit', type=int, default=10, help='Max results')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = search_companies(
            name=args.name,
            domain=args.domain,
            industry=args.industry,
            limit=args.limit
        )

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            companies = result.get('results', [])
            total = result.get('total', len(companies))

            if not companies:
                print("\nNo companies found matching your criteria.")
            else:
                print(f"\nFound {total} company(s):\n")

                for i, company in enumerate(companies, 1):
                    props = company.get('properties', {})
                    print(f"{i}. {props.get('name', 'No name')}")
                    print(f"   ID: {company.get('id')}")
                    if props.get('domain'):
                        print(f"   Domain: {props.get('domain')}")
                    if props.get('industry'):
                        print(f"   Industry: {props.get('industry')}")
                    print()

    except HubSpotError as e:
        if args.json:
            print(json.dumps({'error': True, 'status_code': e.status_code, 'message': e.message}, indent=2))
        else:
            print(f"\n[ERROR] {e.message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
