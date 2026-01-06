#!/usr/bin/env python3
"""
Create HubSpot Company

Creates a new company in HubSpot CRM.

Usage:
    python create_company.py --name NAME [--domain DOMAIN] [--industry INDUSTRY] [--phone PHONE] [--json]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from hubspot_client import get_client, HubSpotError


def create_company(name, domain=None, industry=None, phone=None, **extra_properties):
    """Create a new company in HubSpot."""
    client = get_client()

    properties = {'name': name}

    if domain:
        properties['domain'] = domain
    if industry:
        properties['industry'] = industry
    if phone:
        properties['phone'] = phone

    properties.update(extra_properties)

    return client.post('/crm/v3/objects/companies', {'properties': properties})


def main():
    parser = argparse.ArgumentParser(description='Create HubSpot company')
    parser.add_argument('--name', type=str, required=True, help='Company name (required)')
    parser.add_argument('--domain', type=str, help='Company domain/website')
    parser.add_argument('--industry', type=str, help='Industry')
    parser.add_argument('--phone', type=str, help='Phone number')
    parser.add_argument('--city', type=str, help='City')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = create_company(
            name=args.name,
            domain=args.domain,
            industry=args.industry,
            phone=args.phone,
            city=args.city
        )

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            props = result.get('properties', {})
            print(f"\n[SUCCESS] Company created!")
            print(f"  ID: {result.get('id')}")
            print(f"  Name: {props.get('name')}")
            if props.get('domain'):
                print(f"  Domain: {props.get('domain')}")
            if props.get('industry'):
                print(f"  Industry: {props.get('industry')}")
            print()

    except HubSpotError as e:
        if args.json:
            print(json.dumps({'error': True, 'status_code': e.status_code, 'message': e.message, 'category': e.category}, indent=2))
        else:
            print(f"\n[ERROR] {e.message}")
            if e.category == 'CONFLICT':
                print("  Company may already exist. Use search_companies.py to find it.")
        sys.exit(1)


if __name__ == "__main__":
    main()
