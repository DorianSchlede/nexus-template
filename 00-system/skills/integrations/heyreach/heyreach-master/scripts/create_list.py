#!/usr/bin/env python3
"""
Create HeyReach Lead List

Usage:
    python create_list.py --name NAME [--description DESC] [--json]
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from heyreach_client import get_client, HeyReachError


def create_list(name, description=None):
    client = get_client()
    payload = {"name": name}
    if description:
        payload["description"] = description
    return client.post("/list/CreateEmpty", payload)


def main():
    parser = argparse.ArgumentParser(description='Create lead list')
    parser.add_argument('--name', required=True, help='List name')
    parser.add_argument('--description', help='Optional description')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = create_list(args.name, args.description)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"[OK] Lead list created!")
            print(f"   Name: {result.get('name', args.name)}")
            print(f"   ID: {result.get('id', 'N/A')}")

    except HeyReachError as e:
        if args.json:
            print(json.dumps({"error": True, "status_code": e.status_code, "message": e.message}, indent=2))
        else:
            print(f"Error ({e.status_code}): {e.message}")
        sys.exit(1)
    except ValueError as e:
        if args.json:
            print(json.dumps({"error": True, "message": str(e)}, indent=2))
        else:
            print(f"Config Error: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
