#!/usr/bin/env python3
"""
Update HubSpot Contact

Updates an existing contact in HubSpot CRM.

Usage:
    python update_contact.py --id CONTACT_ID [--email EMAIL] [--firstname NAME] [--lastname NAME] [--phone PHONE] [--json]
"""

import sys
import json
import argparse
from pathlib import Path

# Add scripts directory to path for imports
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from hubspot_client import get_client, HubSpotError


def update_contact(contact_id, **properties):
    """
    Update an existing contact in HubSpot.

    Args:
        contact_id: ID of contact to update
        **properties: Properties to update

    Returns:
        dict with updated contact data
    """
    client = get_client()

    # Filter out None values
    update_props = {k: v for k, v in properties.items() if v is not None}

    if not update_props:
        raise ValueError("No properties provided to update")

    return client.patch(f'/crm/v3/objects/contacts/{contact_id}', {'properties': update_props})


def main():
    parser = argparse.ArgumentParser(description='Update HubSpot contact')
    parser.add_argument('--id', type=str, required=True, help='Contact ID to update')
    parser.add_argument('--email', type=str, help='New email')
    parser.add_argument('--firstname', type=str, help='New first name')
    parser.add_argument('--lastname', type=str, help='New last name')
    parser.add_argument('--phone', type=str, help='New phone number')
    parser.add_argument('--company', type=str, help='New company name')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = update_contact(
            contact_id=args.id,
            email=args.email,
            firstname=args.firstname,
            lastname=args.lastname,
            phone=args.phone,
            company=args.company
        )

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            props = result.get('properties', {})
            name = f"{props.get('firstname', '')} {props.get('lastname', '')}".strip() or 'Contact'

            print(f"\n[SUCCESS] Contact updated!")
            print(f"  ID: {result.get('id')}")
            print(f"  Name: {name}")
            print(f"  Email: {props.get('email')}")
            if props.get('phone'):
                print(f"  Phone: {props.get('phone')}")
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
            if e.category == 'OBJECT_NOT_FOUND':
                print(f"  Contact with ID {args.id} not found.")
        sys.exit(1)
    except ValueError as e:
        if args.json:
            print(json.dumps({'error': True, 'message': str(e)}, indent=2))
        else:
            print(f"\n[ERROR] {str(e)}")
        sys.exit(1)
    except Exception as e:
        if args.json:
            print(json.dumps({'error': True, 'message': str(e)}, indent=2))
        else:
            print(f"\n[ERROR] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
