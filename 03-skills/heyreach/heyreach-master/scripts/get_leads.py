#!/usr/bin/env python3
"""
Get HeyReach Campaign Leads

Usage:
    python get_leads.py --campaign-id ID [--limit N] [--offset N] [--json]
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from heyreach_client import get_client, HeyReachError


def get_leads(campaign_id, limit=100, offset=0):
    client = get_client()
    return client.post("/campaign/GetLeads", {
        "campaignId": campaign_id,
        "offset": offset,
        "limit": limit
    })


def main():
    parser = argparse.ArgumentParser(description='Get campaign leads')
    parser.add_argument('--campaign-id', required=True, help='Campaign ID')
    parser.add_argument('--limit', type=int, default=100, help='Max results')
    parser.add_argument('--offset', type=int, default=0, help='Pagination offset')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = get_leads(args.campaign_id, limit=args.limit, offset=args.offset)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            leads = result.get("items", [])
            total = result.get("totalCount", len(leads))
            print(f"Found {total} leads in campaign:\n")

            for i, lead in enumerate(leads, 1):
                name = f"{lead.get('firstName', '')} {lead.get('lastName', '')}".strip() or "Unknown"
                print(f"{i}. {name}")
                print(f"   Status: {lead.get('status', 'UNKNOWN')}")
                print(f"   LinkedIn: {lead.get('linkedInUrl', 'N/A')}")
                print(f"   ID: {lead.get('id', 'N/A')}\n")

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
