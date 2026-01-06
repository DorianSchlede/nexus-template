#!/usr/bin/env python3
"""
Get HubSpot Associations

Retrieves associations between CRM objects (e.g., contacts linked to a deal).

Usage:
    python get_associations.py --object-type TYPE --object-id ID --to-type TO_TYPE [--json]

Examples:
    python get_associations.py --object-type deals --object-id 123 --to-type contacts
    python get_associations.py --object-type contacts --object-id 456 --to-type companies
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from hubspot_client import get_client, HubSpotError


def get_associations(object_type, object_id, to_object_type):
    """
    Get associations between CRM objects.

    Args:
        object_type: Source object type (contacts, companies, deals)
        object_id: Source object ID
        to_object_type: Target object type

    Returns:
        dict with association results
    """
    client = get_client()

    return client.get(f'/crm/v4/objects/{object_type}/{object_id}/associations/{to_object_type}')


def main():
    parser = argparse.ArgumentParser(description='Get HubSpot associations')
    parser.add_argument('--object-type', type=str, required=True,
                       help='Source object type (contacts, companies, deals)')
    parser.add_argument('--object-id', type=str, required=True,
                       help='Source object ID')
    parser.add_argument('--to-type', type=str, required=True,
                       help='Target object type')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = get_associations(args.object_type, args.object_id, args.to_type)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            associations = result.get('results', [])

            if not associations:
                print(f"\nNo {args.to_type} associated with this {args.object_type[:-1]}.")
            else:
                print(f"\nFound {len(associations)} associated {args.to_type}:\n")

                for i, assoc in enumerate(associations, 1):
                    to_id = assoc.get('toObjectId')
                    assoc_types = assoc.get('associationTypes', [])
                    type_labels = [t.get('label', t.get('typeId')) for t in assoc_types]

                    print(f"{i}. {args.to_type[:-1].title()} ID: {to_id}")
                    if type_labels:
                        print(f"   Association type(s): {', '.join(str(t) for t in type_labels)}")
                    print()

    except HubSpotError as e:
        if args.json:
            print(json.dumps({'error': True, 'status_code': e.status_code, 'message': e.message}, indent=2))
        else:
            print(f"\n[ERROR] {e.message}")
            if e.category == 'OBJECT_NOT_FOUND':
                print(f"  Object not found: {args.object_type}/{args.object_id}")
        sys.exit(1)


if __name__ == "__main__":
    main()
