#!/usr/bin/env python3
"""
List HeyReach Campaigns

Usage:
    python list_campaigns.py [--limit N] [--offset N] [--json]
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from heyreach_client import get_client, HeyReachError


def list_campaigns(limit=100, offset=0):
    client = get_client()
    return client.post("/campaign/GetAll", {"offset": offset, "limit": limit})


def main():
    parser = argparse.ArgumentParser(description='List HeyReach campaigns')
    parser.add_argument('--limit', type=int, default=100, help='Max results')
    parser.add_argument('--offset', type=int, default=0, help='Pagination offset')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = list_campaigns(limit=args.limit, offset=args.offset)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            campaigns = result.get("items", [])
            total = result.get("totalCount", len(campaigns))
            print(f"Found {total} campaigns:\n")

            for i, c in enumerate(campaigns, 1):
                stats = c.get("stats", {})
                print(f"{i}. {c.get('name', 'Unnamed')}")
                print(f"   Status: {c.get('status', 'UNKNOWN')}")
                if stats:
                    print(f"   Leads: {stats.get('totalLeads', 0)} | Contacted: {stats.get('contacted', 0)} | Replied: {stats.get('replied', 0)}")
                print(f"   ID: {c.get('id', 'N/A')}\n")

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
