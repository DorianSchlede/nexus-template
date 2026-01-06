#!/usr/bin/env python3
"""
Create HubSpot Contact

Creates a new contact in HubSpot CRM.

Usage:
    python create_contact.py --email EMAIL [--firstname NAME] [--lastname NAME] [--phone PHONE] [--company COMPANY] [--json]
"""

import sys
import json
import argparse
from pathlib import Path

# Add scripts directory to path for imports
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from hubspot_client import get_client, HubSpotError


def create_contact(email, firstname=None, lastname=None, phone=None, company=None, **extra_properties):
    """
    Create a new contact in HubSpot.

    Args:
        email: Contact email (required)
        firstname: First name
        lastname: Last name
        phone: Phone number
        company: Company name
        **extra_properties: Additional properties

    Returns:
        dict with created contact data
    """
    client = get_client()

    properties = {'email': email}

    if firstname:
        properties['firstname'] = firstname
    if lastname:
        properties['lastname'] = lastname
    if phone:
        properties['phone'] = phone
    if company:
        properties['company'] = company

    properties.update(extra_properties)

    return client.post('/crm/v3/objects/contacts', {'properties': properties})


def main():
    parser = argparse.ArgumentParser(description='Create HubSpot contact')
    parser.add_argument('--email', type=str, required=True, help='Contact email (required)')
    parser.add_argument('--firstname', type=str, help='First name')
    parser.add_argument('--lastname', type=str, help='Last name')
    parser.add_argument('--phone', type=str, help='Phone number')
    parser.add_argument('--company', type=str, help='Company name')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = create_contact(
            email=args.email,
            firstname=args.firstname,
            lastname=args.lastname,
            phone=args.phone,
            company=args.company
        )

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            contact_id = result.get('id')
            props = result.get('properties', {})
            name = f"{props.get('firstname', '')} {props.get('lastname', '')}".strip() or args.email

            print(f"\n[SUCCESS] Contact created!")
            print(f"  ID: {contact_id}")
            print(f"  Name: {name}")
            print(f"  Email: {props.get('email')}")
            if props.get('phone'):
                print(f"  Phone: {props.get('phone')}")
            if props.get('company'):
                print(f"  Company: {props.get('company')}")
            print()

    except HubSpotError as e:
        if args.json:
            print(json.dumps({
                'error': True,
                'status_code': e.status_code,
                'message': e.message,
                'category': e.category,
                'errors': e.errors
            }, indent=2))
        else:
            print(f"\n[ERROR] {e.message}")
            if e.category == 'CONFLICT':
                print("  Contact with this email already exists.")
                print("  Use search_contacts.py to find the existing contact.")
            elif e.category == 'VALIDATION_ERROR':
                for error in e.errors:
                    print(f"  - {error.get('name', 'Field')}: {error.get('message', 'Invalid')}")
        sys.exit(1)
    except Exception as e:
        if args.json:
            print(json.dumps({'error': True, 'message': str(e)}, indent=2))
        else:
            print(f"\n[ERROR] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
