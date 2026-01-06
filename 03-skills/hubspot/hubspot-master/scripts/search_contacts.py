#!/usr/bin/env python3
"""
Search HubSpot Contacts

Searches contacts in HubSpot CRM by various criteria.

Usage:
    python search_contacts.py [--email EMAIL] [--name NAME] [--company COMPANY] [--limit N] [--json]
"""

import sys
import json
import argparse
from pathlib import Path

# Add scripts directory to path for imports
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from hubspot_client import get_client, HubSpotError


def search_contacts(email=None, name=None, company=None, limit=10):
    """
    Search contacts in HubSpot.

    Args:
        email: Search by email (exact match)
        name: Search by name (contains)
        company: Search by company (contains)
        limit: Max results

    Returns:
        dict with search results
    """
    client = get_client()

    filters = []

    if email:
        filters.append({
            'propertyName': 'email',
            'operator': 'EQ',
            'value': email
        })

    if name:
        # Search both first and last name
        filters.append({
            'propertyName': 'firstname',
            'operator': 'CONTAINS_TOKEN',
            'value': name
        })
        # Note: HubSpot doesn't support OR in a single filter group for different fields
        # We'll search firstname first, then lastname if no results

    if company:
        filters.append({
            'propertyName': 'company',
            'operator': 'CONTAINS_TOKEN',
            'value': company
        })

    if not filters:
        # No filters - just return recent contacts
        return client.get('/crm/v3/objects/contacts', params={
            'limit': limit,
            'properties': 'email,firstname,lastname,phone,company'
        })

    search_body = {
        'filterGroups': [{'filters': filters}],
        'properties': ['email', 'firstname', 'lastname', 'phone', 'company'],
        'limit': limit
    }

    result = client.post('/crm/v3/objects/contacts/search', search_body)

    # If searching by name and no results, try lastname
    if name and not result.get('results') and not email:
        search_body['filterGroups'] = [{
            'filters': [{
                'propertyName': 'lastname',
                'operator': 'CONTAINS_TOKEN',
                'value': name
            }]
        }]
        result = client.post('/crm/v3/objects/contacts/search', search_body)

    return result


def main():
    parser = argparse.ArgumentParser(description='Search HubSpot contacts')
    parser.add_argument('--email', type=str, help='Search by email (exact match)')
    parser.add_argument('--name', type=str, help='Search by name (first or last)')
    parser.add_argument('--company', type=str, help='Search by company')
    parser.add_argument('--limit', type=int, default=10, help='Max results')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = search_contacts(
            email=args.email,
            name=args.name,
            company=args.company,
            limit=args.limit
        )

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            contacts = result.get('results', [])
            total = result.get('total', len(contacts))

            if not contacts:
                print("\nNo contacts found matching your criteria.")
            else:
                print(f"\nFound {total} contact(s):\n")

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

    except HubSpotError as e:
        if args.json:
            print(json.dumps({
                'error': True,
                'status_code': e.status_code,
                'message': e.message,
                'category': e.category
            }, indent=2))
        else:
            print(f"\n[ERROR] {e.message}")
        sys.exit(1)
    except Exception as e:
        if args.json:
            print(json.dumps({'error': True, 'message': str(e)}, indent=2))
        else:
            print(f"\n[ERROR] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
