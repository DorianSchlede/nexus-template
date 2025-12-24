#!/usr/bin/env python3
"""
List HeyReach Lead Lists

Usage:
    python list_lists.py [--limit N] [--json]
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from heyreach_client import get_client, HeyReachError


def list_lists(limit=100, offset=0):
    client = get_client()
    return client.post("/list/GetAll", {"offset": offset, "limit": limit})


def main():
    parser = argparse.ArgumentParser(description='List lead lists')
    parser.add_argument('--limit', type=int, default=100, help='Max results')
    parser.add_argument('--offset', type=int, default=0, help='Pagination offset')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = list_lists(args.limit, args.offset)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            lists = result.get("items", [])
            total = result.get("totalCount", len(lists))
            print(f"Found {total} lead lists:\n")

            for i, lst in enumerate(lists, 1):
                print(f"{i}. {lst.get('name', 'Unnamed')}")
                print(f"   Leads: {lst.get('leadCount', 0)}")
                print(f"   ID: {lst.get('id', 'N/A')}\n")

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
