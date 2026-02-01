#!/usr/bin/env python3
"""
List HubSpot Contacts

Retrieves contacts from HubSpot CRM with pagination support.

Usage:
    python list_contacts.py [--limit N] [--properties PROPS] [--after CURSOR] [--json]
"""

import sys
import json
import argparse
from pathlib import Path

# Add scripts directory to path for imports
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from hubspot_client import get_client, HubSpotError


def list_contacts(limit=10, properties=None, after=None):
    """
    List contacts from HubSpot.

    Args:
        limit: Number of results (max 100)
        properties: List of property names to include
        after: Pagination cursor

    Returns:
        dict with results and paging info
    """
    client = get_client()

    if properties is None:
        properties = ['email', 'firstname', 'lastname', 'phone', 'company']

    params = {
        'limit': min(limit, 100),
        'properties': ','.join(properties) if isinstance(properties, list) else properties
    }

    if after:
        params['after'] = after

    return client.get('/crm/v3/objects/contacts', params=params)


def main():
    parser = argparse.ArgumentParser(description='List HubSpot contacts')
    parser.add_argument('--limit', type=int, default=10, help='Number of results (max 100)')
    parser.add_argument('--properties', type=str, default='email,firstname,lastname,phone,company',
                       help='Comma-separated property names')
    parser.add_argument('--after', type=str, help='Pagination cursor')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        properties = args.properties.split(',') if args.properties else None
        result = list_contacts(args.limit, properties, args.after)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            contacts = result.get('results', [])
            print(f"\nFound {len(contacts)} contacts:\n")

            for i, contact in enumerate(contacts, 1):
                props = contact.get('properties', {})
                name = f"{props.get('firstname', '')} {props.get('lastname', '')}".strip() or 'No name'
                email = props.get('email', 'No email')
                company = props.get('company', '')

                print(f"{i}. {name}")
                print(f"   Email: {email}")
                print(f"   ID: {contact.get('id')}")
                if company:
                    print(f"   Company: {company}")
                print()

            # Pagination info
            paging = result.get('paging', {})
            if paging.get('next'):
                print(f"More results available. Use --after {paging['next']['after']}")

    except HubSpotError as e:
        if args.json:
            print(json.dumps({
                'error': True,
                'status_code': e.status_code,
                'message': e.message,
                'category': e.category
            }, indent=2))
        else:
            print(f"Error: {e.message}")
            if e.category:
                print(f"Category: {e.category}")
        sys.exit(1)
    except Exception as e:
        if args.json:
            print(json.dumps({'error': True, 'message': str(e)}, indent=2))
        else:
            print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
